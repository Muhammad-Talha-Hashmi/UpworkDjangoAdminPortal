from django.db import models

# Create your models here.


class User(models.Model):
    username = models.TextField()
    email = models.EmailField(max_length=254)
    fullname = models.CharField(max_length=150)
    password = models.TextField()
    profile_picture = models.ImageField(
        upload_to="media/profile_pictures", null=True, blank=True)
    role = models.CharField(max_length=45, default="Researcher")
    university = models.TextField()
    department = models.TextField()
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    office_number = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(max_length=45, default="Pending")


class Journal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    publisher = models.TextField()
    publish_year = models.PositiveIntegerField()
    category = models.TextField()
    department = models.TextField()
    rank = models.CharField(max_length=45)
    status = models.CharField(max_length=45, default="Waiting")


class Research(models.Model):
    title = models.TextField()
    author = models.TextField()
    other_author = models.TextField()
    abstract = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=False)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    research_url = models.URLField(max_length=200)
    journal_name = models.TextField()
    category = models.TextField()
    department = models.TextField()


class Cateogry(models.Model):
    choices = (
        ("clinical_sciences", "Clinical Sciences"),
        ("dietitian_and_nutritionist", "Dietitian and Nutritionist"),
        ("laboratory_science", "Laboratory Science"),
        ("otolaryngology", "Otolaryngology"),
        ("physical_therapy", "Physical Therapy"),
        ("therapy_and_rehabilitation", "Therapy and Rehabilitation")
    )
    name = models.CharField(max_length=100, choices=choices)


class FavorableJournal(models.Model):
    user = models.ForeignKey("adminsite.User", on_delete=models.CASCADE)
    journal = models.ForeignKey("adminsite.Journal", on_delete=models.CASCADE)


class FavorableResearch(models.Model):
    user = models.ForeignKey("adminsite.User", on_delete=models.CASCADE)
    research = models.ForeignKey(
        "adminsite.Research", on_delete=models.CASCADE)


class GuestFeedback(models.Model):
    name = models.CharField(max_length=50)
    reason = models.TextField()
    feedback = models.CharField(max_length=50)
    additional_comment = models.CharField(max_length=50)


class ProjectGroup(models.Model):
    title = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    starting_date = models.DateField(auto_now=False, auto_now_add=False)
    finishing_date = models.DateField(auto_now=False, auto_now_add=False)
    member1 = models.TextField()
    member2 = models.TextField()
    member3 = models.TextField()
    member4 = models.TextField()
    member5 = models.TextField()
    member6 = models.TextField()


class NewMilestone(models.Model):
    project = models.ForeignKey(
        "adminsite.ProjectGroup", on_delete=models.CASCADE)
    milestone_type = models.CharField(max_length=50)
    starting_date = models.DateField(auto_now=False, auto_now_add=False)
    finishing_date = models.DateField(auto_now=False, auto_now_add=False)
    file = models.FileField(upload_to="files/", max_length=100)
    additional_comment = models.TextField()


class PublicationMilestone(models.Model):
    project = models.ForeignKey(
        "adminsite.ProjectGroup", on_delete=models.CASCADE)
    journal = models.ForeignKey("adminsite.Journal", on_delete=models.CASCADE)
    submittion_date = models.DateField(auto_now=False, auto_now_add=False)
    rejection_date = models.DateField(auto_now=False, auto_now_add=False)
    first_comment_date = models.DateField(auto_now=False, auto_now_add=False)
    end_review_date = models.DateField(auto_now=False, auto_now_add=False)
    final_acceptance_date = models.DateField(
        auto_now=False, auto_now_add=False)
    final_publication_date = models.DateField(
        auto_now=False, auto_now_add=False)
    feedback = models.TextField()

