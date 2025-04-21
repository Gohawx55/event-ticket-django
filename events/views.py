from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.core.files.storage import default_storage

from .models import Event, Ticket
from django.db.models import Q

# PDF генерация
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os


def event_list(request):
    query = request.GET.get('q')
    if query:
        events = Event.objects.filter(title__icontains=query)
    else:
        events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity > event.available_seats:
            messages.error(request, 'Недостаточно свободных мест.')
            return redirect('buy_ticket', event_id=event.id)

        event.available_seats -= quantity
        event.save()

        Ticket.objects.create(
            event=event,
            buyer=request.user,
            quantity=quantity
        )
        messages.success(request, 'Билет успешно куплен!')
        return redirect('my_tickets')

    return render(request, 'events/buy_ticket.html', {'event': event})


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(buyer=request.user)
    return render(request, 'events/my_tickets.html', {'tickets': tickets})


@login_required
def profile(request):
    tickets = Ticket.objects.filter(buyer=request.user)
    total_tickets = sum(ticket.quantity for ticket in tickets)
    return render(request, 'events/profile.html', {
        'tickets': tickets,
        'total_tickets': total_tickets
    })



@login_required
def download_ticket_pdf(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, buyer=request.user)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    
    elements.append(Paragraph("🎟 Электронный билет", styles['Title']))
    elements.append(Spacer(1, 12))

    
    elements.append(Paragraph(f"<b>Событие:</b> {ticket.event.title}", styles['Normal']))
    elements.append(Paragraph(f"<b>Дата:</b> {ticket.event.date}", styles['Normal']))
    elements.append(Paragraph(f"<b>Количество:</b> {ticket.quantity}", styles['Normal']))
    elements.append(Paragraph(f"<b>Покупатель:</b> {request.user.username}", styles['Normal']))
    elements.append(Spacer(1, 12))

    
    logo_path = os.path.join(settings.BASE_DIR, 'events', 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=60*mm, height=20*mm))
        elements.append(Spacer(1, 12))

    
    if ticket.qr_code and os.path.exists(ticket.qr_code.path):
        elements.append(Paragraph("<b>QR-код билета:</b>", styles['Normal']))
        elements.append(Image(ticket.qr_code.path, width=50*mm, height=50*mm))

    doc.build(elements)
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'ticket_{ticket.id}.pdf')
