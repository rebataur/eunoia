# Generated by Django 3.0 on 2020-03-17 07:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivitySequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.IntegerField(default=0)),
                ('order', models.IntegerField(default=0)),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BrainStorm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=1024)),
                ('created_on', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ability_for', models.CharField(max_length=30)),
                ('ability_to', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=10240)),
                ('priority', models.CharField(choices=[('MUST_HAVE', 'Must Have'), ('SHOULD_HAVE', 'Should Have'), ('COULD_HAVE', 'Could Have'), ('WOULD_HAVE', 'Would Have')], max_length=30)),
                ('tag', models.CharField(blank=True, max_length=1024, null=True)),
                ('outcome', models.CharField(max_length=1024)),
                ('value', models.CharField(max_length=1024)),
                ('complexity', models.CharField(choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low'), ('VERY_LOW', 'Very Low'), ('UNKNOWN', 'Unknown')], max_length=30, null=True)),
                ('status', models.CharField(choices=[('TODO', 'Todo'), ('IN_PROGRESS', 'In Progress'), ('DONE', 'Done'), ('POSTPONED', 'Postponed'), ('WAITING_ON', 'WAITING_ON')], default='TODO', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_id', models.IntegerField(default=0)),
                ('order', models.IntegerField(default=0)),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea_name', models.CharField(max_length=30)),
                ('intended_persona', models.CharField(max_length=1024)),
                ('core_concept', models.CharField(max_length=10240)),
                ('my_strength', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(choices=[('INCUBATING', 'Incubating'), ('PRODUCTIZE', 'Productize'), ('ATTIC', 'Attic')], default='INCUBATING', max_length=30)),
                ('created_on', models.DateField(default=datetime.datetime.now)),
                ('brainstorming', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.BrainStorm')),
            ],
        ),
        migrations.CreateModel(
            name='IdeaNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024)),
                ('created_on', models.DateField(default=datetime.datetime.now)),
                ('arhive', models.BooleanField(blank=True, default=False, null=True)),
                ('updated_on', models.DateField(default=datetime.datetime.now)),
                ('belongs_to_brainstorm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eunoiaapp.BrainStorm')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('overview', models.CharField(max_length=1024)),
                ('epic', models.CharField(max_length=1024)),
                ('idea', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Idea')),
            ],
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.CharField(default='In order to <receive benefit> as a <role>, I can <goal/desire>', max_length=1024)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eunoiaapp.Feature')),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eunoiaapp.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('profile_pic', models.ImageField(default='/media/profile_pics/placeholder_profile_pic.png', upload_to='profile_pics/')),
                ('tenant_id', models.CharField(blank=True, max_length=30)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('country', models.CharField(blank=True, max_length=30)),
                ('zip_code', models.IntegerField(blank=True, default=0, null=True)),
                ('company_name', models.CharField(max_length=30)),
                ('role', models.CharField(choices=[('FOUNDER', 'Founder'), ('CEO', 'CEO'), ('PO', 'Product Owner'), ('SCRUM_MASTER', 'Scrum Master'), ('DEVELOPER', 'Developer')], max_length=30)),
                ('employee_id', models.CharField(max_length=30)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Profile'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('sent', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IdeaNoteAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=30)),
                ('belongs_to_ideanote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eunoiaapp.IdeaNote')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='ideanote',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Profile'),
        ),
        migrations.AddField(
            model_name='idea',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Profile'),
        ),
        migrations.AddField(
            model_name='feature',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='feature_created_by_set', to='eunoiaapp.Profile'),
        ),
        migrations.AddField(
            model_name='feature',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Product'),
        ),
        migrations.AddField(
            model_name='brainstorm',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Profile'),
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BUSINESS', 'Business'), ('TECHNICAL', 'Technical'), ('INFRASTRUCTURE', 'Infrastructure')], max_length=30, null=True)),
                ('complexity', models.CharField(choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low'), ('VERY_LOW', 'Very Low'), ('UNKNOWN', 'Unknown')], max_length=30, null=True)),
                ('status', models.CharField(choices=[('TODO', 'Todo'), ('IN_PROGRESS', 'In Progress'), ('DONE', 'Done'), ('POSTPONED', 'Postponed'), ('WAITING_ON', 'Waiting On')], default='TODO', max_length=30, null=True)),
                ('outcome', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=1024, null=True)),
                ('note', models.CharField(max_length=1024, null=True)),
                ('created_on', models.DateField(default=datetime.datetime.now)),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assignedto_by_set', to='eunoiaapp.Profile')),
                ('belongs_to_sprint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Sprint')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_by_set', to='eunoiaapp.Profile')),
                ('depends_on', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eunoiaapp.Activity')),
                ('related_to_feature', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Feature')),
                ('related_to_idea', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.Idea')),
                ('user_story', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eunoiaapp.UserStory')),
            ],
        ),
    ]
