from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# =========================
# PAGE D'ACCUEIL
# =========================
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


# =========================
# CONNEXION
# =========================
def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        error = "Nom d'utilisateur ou mot de passe incorrect."

    return render(request, "core/login.html", {"error": error})


# =========================
# INSCRIPTION
# =========================
def signup_view(request):
    form = UserCreationForm(request.POST or None)

    email = ""
    email_error = ""
    role_error = ""
    selected_role = ""

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        selected_role = request.POST.get("role", "").strip()

        # Vérifier l'adresse e-mail
        if not email:
            email_error = "Veuillez saisir votre adresse e-mail."
        else:
            try:
                validate_email(email)
            except ValidationError:
                email_error = "Veuillez saisir une adresse e-mail valide."

        # Vérifier le rôle choisi
        if selected_role not in ["participant", "organisateur"]:
            role_error = "Veuillez choisir un type de compte valide."

        # Créer le compte si tous les champs sont valides
        if form.is_valid() and not email_error and not role_error:
            user = form.save(commit=False)
            user.email = email
            user.save()

            # Créer ou récupérer le groupe correspondant au rôle
            group_name = (
                "Participant"
                if selected_role == "participant"
                else "Organisateur"
            )

            group, created = Group.objects.get_or_create(
                name=group_name
            )

            # Associer le compte au groupe
            user.groups.add(group)

            # Connecter automatiquement le nouvel utilisateur
            login(request, user)

            return redirect("home")

    contexte = {
        "form": form,
        "email": email,
        "email_error": email_error,
        "role_error": role_error,
        "selected_role": selected_role,
    }

    return render(request, "core/signup.html", contexte)
