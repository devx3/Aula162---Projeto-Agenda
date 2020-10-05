from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.core.paginator import Paginator
from .models import Contact
from django.http import HttpResponse
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request) -> HttpResponse:
    contacts_list = Contact.objects.order_by('-id').filter(
        enabled=True
    )
    paginator = Paginator(contacts_list, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })


def contact(request, contact_id) -> HttpResponse:
    contact = get_object_or_404(Contact, id=contact_id)

    if not contact.enabled:
        raise Http404()
    return render(request, 'contacts/contact.html', {
        'contact': contact
    })


def search(request) -> HttpResponse:
    term = request.GET.get('term')

    if term is None or not term:
        # raise Http404()
        messages.add_message(request, messages.ERROR, 'Campo busca não pode ficar vazio.')
        return redirect('index')

    fields = Concat('firstname', Value(' '), 'lastname')
    contacts_list = Contact.objects.annotate(
        fullname=fields
    ).filter(
        Q(fullname__icontains=term) | Q(phone__icontains=term)
    )
    paginator = Paginator(contacts_list, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, 'contacts/search.html', {
        'contacts': contacts
    })
