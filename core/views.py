
from django.shortcuts import render


def home(request):
    evenements = [
        {
            "titre": "Conférence Tech & Innovation",
            "categorie": "Technologie",
            "date": "24 octobre 2026",
            "lieu": "Tunis, Tunisie",
            "prix": "Gratuit",
            "image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=900&q=80",
        },
        {
            "titre": "Atelier créatif",
            "categorie": "Art & Culture",
            "date": "28 octobre 2026",
            "lieu": "Sousse, Tunisie",
            "prix": "20 DT",
            "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=900&q=80",
        },
        {
            "titre": "Rencontre des entrepreneurs",
            "categorie": "Business",
            "date": "2 novembre 2026",
            "lieu": "Sfax, Tunisie",
            "prix": "Gratuit",
            "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=900&q=80",
        },
    ]

    recherche = request.GET.get("q", "").strip()
    lieu_recherche = request.GET.get("lieu", "").strip()

    evenements = [
        evenement
        for evenement in evenements
        if (
            not recherche
            or recherche.casefold() in evenement["titre"].casefold()
            or recherche.casefold() in evenement["categorie"].casefold()
            or recherche.casefold() in evenement["lieu"].casefold()
        )
        and (
            not lieu_recherche
            or lieu_recherche.casefold() in evenement["lieu"].casefold()
        )
    ]

    contexte = {
        "evenements": evenements,
        "recherche": recherche,
        "lieu_recherche": lieu_recherche,
    }

    return render(request, "core/home.html", contexte)
