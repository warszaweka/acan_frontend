import ffmpeg
from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.files.storage import default_storage
from django.forms import CharField, ModelForm, PasswordInput
from modeltranslation.admin import TranslationAdmin

from .models import Course, Lesson, Order, User


@register(Course)
class CourseAdmin(TranslationAdmin):
    list_display = ('title', 'cost', 'published', 'soon')
    list_filter = ('published', 'soon')
    search_fields = ('title', )
    ordering = ('title', 'cost')


@register(Lesson)
class LessonAdmin(TranslationAdmin):
    list_display = ('order', 'title', 'course')
    search_fields = ('title', 'course')
    ordering = ('order', 'title', 'course')

    def save_model(self, request, obj, *args, **kwargs):
        super().save_model(request, obj, *args, **kwargs)
        old_video = obj.video
        new_video = f'lesson_{obj.id}_.m3u8'
        new_video_path = default_storage.path(new_video)
        ffmpeg.input(old_video.path).output(new_video_path,
                                            acodec='aac',
                                            vcodec='copy',
                                            start_number=0,
                                            hls_time=10,
                                            hls_list_size=0,
                                            f='hls').run()
        old_video.delete(save=False)
        obj.video = new_video
        obj.save()


class UserCreationForm(ModelForm):
    password = CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'mailing_list')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ('mailing_list', 'is_staff')


@register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone', 'first_name', 'last_name',
                    'mailing_list', 'is_staff', 'is_active')
    list_filter = ('mailing_list', 'is_staff', 'is_active')
    fieldsets = ((None, {'fields': ('mailing_list', 'is_staff')}), )
    add_fieldsets = ((None, {
        'fields': ('email', 'password', 'phone', 'first_name', 'last_name',
                   'mailing_list'),
    }), )
    search_fields = ('email', 'phone', 'first_name', 'last_name')
    ordering = ('email', 'phone', 'first_name', 'last_name')


site.unregister(Group)


@register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('course', 'user', 'payed')
    list_filter = ('payed', )
    search_fields = ('course', 'user')
    ordering = ('course', 'user')
