from django.db import models


class Category(models.Model):
    category_name = models.CharField(primary_key=True, max_length=70)

    class Meta:
        managed = False
        db_table = 'category'




class Journals(models.Model):
    journal_name = models.CharField(db_column='journal_Name', primary_key=True, max_length=100)  # Field name made lowercase.
    publisher = models.TextField()
    main_category = models.TextField()
    quartile_rank = models.CharField(max_length=45)
    status = models.CharField(max_length=45)

    class Meta:
        # managed = False
        db_table = 'journals'





class ProjectGroup(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=45)
    catagory = models.CharField(max_length=45)
    auther_name = models.CharField(max_length=45)
    starting_date = models.DateField()
    finishing_date = models.DateField()
    member1 = models.TextField(blank=True, null=True)
    member2 = models.TextField(blank=True, null=True)
    member3 = models.TextField(blank=True, null=True)
    member4 = models.TextField(blank=True, null=True)
    member5 = models.TextField(blank=True, null=True)
    member6 = models.TextField(blank=True, null=True)
    des = models.TextField(blank=True, null=True)
    created_on = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'project_group'
        unique_together = (('project_id', 'title'),)




class Users(models.Model):
    fullname = models.TextField()
    email = models.TextField()
    username = models.CharField(max_length=45)
    user_profile_picture = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=45)
    university = models.TextField()
    department = models.TextField()
    mobile_number = models.IntegerField(blank=True, null=True)
    office_number = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=45)
    # user_id = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=145, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'users'
        unique_together = (('id', 'username'),)


class ResearchesList(models.Model):
    research_id = models.AutoField(primary_key=True)
    title = models.TextField()
    auther = models.CharField(max_length=45)
    auther1 = models.TextField(blank=True, null=True)
    auther2 = models.TextField(blank=True, null=True)
    auther3 = models.TextField(blank=True, null=True)
    auther4 = models.TextField(blank=True, null=True)
    auther5 = models.TextField(blank=True, null=True)
    auther6 = models.TextField(blank=True, null=True)
    abstract = models.TextField()
    publish_date = models.DateField()
    start_date = models.DateField()
    finish_date = models.DateField()
    research_url = models.TextField()
    journal_name = models.CharField(max_length=100)
    research_category = models.CharField(max_length=70)
    data_type = models.CharField(max_length=45, blank=True, null=True)
    data_source = models.TextField(blank=True, null=True)
    geo_area = models.CharField(max_length=45, blank=True, null=True)
    is_collected_via_socialmedia = models.CharField(max_length=45, blank=True, null=True)
    collecation_start_date = models.DateField(blank=True, null=True)
    finishing_colleaction_date = models.DateField(blank=True, null=True)
    date_of_the_data = models.DateField(blank=True, null=True)
    sample_size = models.IntegerField(blank=True, null=True)
    sampling_method = models.TextField(blank=True, null=True)
    data_collecation = models.TextField(blank=True, null=True)
    data_analysis = models.TextField(blank=True, null=True)
    write_up = models.TextField(blank=True, null=True)
    publication = models.TextField(blank=True, null=True)
    capcity_of_building = models.TextField(blank=True, null=True)
    varisble_and_data_dic_name = models.CharField(max_length=100, blank=True, null=True)
    actual_data_name = models.TextField(blank=True, null=True)
    name_of_the_file = models.TextField(blank=True, null=True)
    file_format = models.CharField(max_length=45, blank=True, null=True)
    file = models.CharField(max_length=100, blank=True, null=True)
    lesson_learnt = models.TextField(blank=True, null=True)
    other_comment = models.TextField(blank=True, null=True)
    is_this_data_public = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    # user_id = models.IntegerField(db_column='user-id', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    user = models.ForeignKey(Users, blank=True, related_name="user_fk",  null=True, on_delete=models.CASCADE)
  # Field renamed to remove unsuitable characters.

    class Meta:
        # managed = False
        db_table = 'researches_list'


