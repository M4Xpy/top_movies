from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import OuterRef, Subquery, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    CustomerCreationForm,
    ActorForm,
    ActorSearchForm,
    CountryForm,
    CountrySearchForm, GenreSearchForm, FilmForm, MovieSearchForm, TopicSearchForm,
)
from .models import (
    Customer,
    Film,
    Country,
    Actor,
    Genre,
    Rate,
    Commentary,
    Topic,
)


def index(request):
    """View function for the home page of the site."""

    num_customers = Customer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_customers": num_customers,
        "num_visits": num_visits + 1,
        "num_movies": Film.objects.count(),
        "num_actors": Actor.objects.count(),
        "num_countries": Country.objects.count(),
        "num_genres": Genre.objects.count(),
        "num_topics": Topic.objects.count(),
        "num_commentaries": Commentary.objects.count(),
    }

    return render(request, "films/index.html", context=context)


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    form_class = CustomerCreationForm


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    success_url = reverse_lazy("")


class ActorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy("films:actor-list")


class ActorListView(generic.ListView):
    model = Actor
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ActorListView, self).get_context_data(**kwargs)
        context["search_form"] = ActorSearchForm(
            initial={"full_name": self.request.GET.get("full_name", "")}
        )

        return context

    def get_queryset(self):
        queryset = Actor.objects.select_related("country").prefetch_related(
            "films_actors__genre",
        )

        full_name = self.request.GET.get("full_name")
        country_id = self.request.GET.get("country_id")
        if full_name:
            return queryset.filter(
                models.Q(name__icontains=full_name)
                | models.Q(surname__icontains=full_name)
            )
        if country_id:
            return queryset.filter(country__id=country_id)

        queryset = queryset.annotate(
            genre_count=Count("films_actors__genre", distinct=True),
            topic_count=Count("films_actors__topics", distinct=True),
        )

        return queryset


class ActorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy("films:actor-list")


class ActorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Actor
    template_name = "includes/delete_confirmation.html"
    success_url = reverse_lazy("films:actor-list")


class CountryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy("films:country-list")


class CountryListView(generic.ListView):
    model = Country
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        context["search_form"] = CountrySearchForm(
            initial={"name": self.request.GET.get("name", "")}
        )
        return context

    def get_queryset(self):
        queryset = Country.objects.prefetch_related(
            "films_country",
            "actors",
            "films_country__topics",
            "films_country__genre",
        )
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        queryset = queryset.annotate(
            genre_count=Count("films_country__genre", distinct=True),
            topic_count=Count("films_country__topics", distinct=True),
        )
        return queryset


class CountryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy("films:country-list")


class CountryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Country
    template_name = "includes/delete_confirmation.html"
    success_url = reverse_lazy("films:country-list")


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("films:genre-list")


class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        context["search_form"] = GenreSearchForm(
            initial={"genre": self.request.GET.get("genre", "")}
        )

        return context

    def get_queryset(self):
        queryset = Genre.objects.prefetch_related(
            "films_genre__actors",
        )
        genre = self.request.GET.get("genre")
        country_id = self.request.GET.get("country_id")
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if country_id:
            queryset = queryset.filter(films_genre__country__id=country_id)
        queryset = queryset.annotate(
            topic_count=Count("films_genre__topics", distinct=True),
            actor_count=Count("films_genre__actors", distinct=True),
        )
        return queryset


class GenreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("films:genre-list")


class GenreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Genre
    template_name = "includes/delete_confirmation.html"
    success_url = reverse_lazy("films:genre-list")


class MovieCreateView(LoginRequiredMixin, generic.CreateView):
    model = Film
    form_class = FilmForm
    success_url = reverse_lazy("films:movie-list")


class MovieListView(generic.ListView):
    model = Film
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        context["search_form"] = MovieSearchForm(
            initial={"film_name": self.request.GET.get("film_name", "")}
        )
        return context

    def get_queryset(self):
        rate_queryset = Rate.objects.filter(
            customer_id=self.request.user.id, film_id=OuterRef("pk")
        )
        queryset = Film.objects.prefetch_related(
            "actors",
            "country",
            "genre",
            "film_rates",
            "film_commentaries",
            "topics",
        )
        film_name = self.request.GET.get("film_name")
        country_id = self.request.GET.get("country_id")
        genre_id = self.request.GET.get("genre_id")
        actor_id = self.request.GET.get("actor_id")
        film_year = self.request.GET.get("film_year")
        topics_id = self.request.GET.get("topic_id")

        if topics_id:
            queryset = queryset.filter(topics__id=topics_id)
        if film_year:
            queryset = queryset.filter(film_year=film_year)
        if film_name:
            queryset = queryset.filter(film_name__icontains=film_name)
        if country_id:
            queryset = queryset.filter(country__id=country_id)
        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        if actor_id:
            queryset = queryset.filter(actors__id=actor_id)
        queryset = queryset.annotate(
            personal_rate=Subquery(rate_queryset.values("rating")[:1])
        )

        return queryset


class MovieDetailView(generic.DetailView):
    model = Film


class MovieUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Film
    form_class = FilmForm
    success_url = reverse_lazy("films:movie-list")


class MovieDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Film
    success_url = reverse_lazy("films:movie-list")


@login_required
def rate_film(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    customer = get_object_or_404(Customer, id=request.user.id)
    new_rating = int(request.POST.get("rating"))
    existing_rate = Rate.objects.filter(customer=customer, film=film).first()

    if existing_rate:
        existing_rate.rating = new_rating
        existing_rate.save()
    else:
        Rate.objects.create(customer=customer, rating=new_rating, film=film)

    return HttpResponseRedirect(reverse_lazy("films:movie-detail",
                                             args=[film_id]))


@login_required
def commentary_film(request, film_id):
    text = request.POST.get("commentary")
    if text:
        Commentary.objects.create(
            owner=get_object_or_404(Customer, id=request.user.id),
            movie=get_object_or_404(Film, id=film_id),
            content=text,
        )

    return HttpResponseRedirect(reverse_lazy("films:movie-detail",
                                             args=[film_id]))


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("films:topic-list")


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        context["search_form"] = TopicSearchForm(
            initial={"topic": self.request.GET.get("topic", "")}
        )

        return context

    def get_queryset(self):
        queryset = Topic.objects.prefetch_related(
            "films_topics__actors",
        )
        topic = self.request.GET.get("topic")
        if topic:
            return queryset.filter(name__icontains=topic)
        queryset = queryset.annotate(
            genre_count=Count("films_topics__genre", distinct=True),
            actor_count=Count("films_topics__actors", distinct=True),
        )
        return queryset
