import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from controller.models import TimeStampedModel

BLOOD_GROUP_CHOICES = (
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
)


class Teacher(TimeStampedModel):
    uid = models.UUIDField(editable=False)
    code = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.TextField()
    qualifications = models.TextField()
    dob = models.DateField()
    experiences = models.TextField()
    department = models.CharField(max_length=50)
    blood_type = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    photo = models.ImageField(upload_to="teachers/photos/%Y", null=True, blank=True)
    cv = models.FileField(upload_to="teachers/cv/%Y", null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        return super(Teacher, self).save(*args, **kwargs)

    @property
    def qualification_list(self):
        if not self.qualifications:
            return []
        return [q.strip() for q in self.qualifications.split(',') if q.strip()]

    @property
    def experience_list(self):
        if not self.experiences:
            return []
        return [e.strip() for e in self.experiences.split(',') if e.strip()]


class SchoolClass(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"


class Subject(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class SubjectClass(TimeStampedModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.code} - {self.teacher.code}"


def student_photo_path(instance, filename):
    return f"students/photos/{instance.name}/{filename}"


class Student(TimeStampedModel):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default="M")
    reg_number = models.CharField(max_length=20, unique=True)
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True)
    dob = models.DateField()
    health_issues = models.TextField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    photo = models.ImageField(upload_to=student_photo_path, null=True, blank=True)
    admission_date = models.DateField(default=timezone.localdate())

    def __str__(self):
        return self.name

    @property
    def health_issue_list(self):
        if not self.health_issues:
            return []
        return [e.strip() for e in self.health_issues.split(',') if e.strip()]


class AcademicYear(TimeStampedModel):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.start_date.strftime("%B %Y")


class Enrollment(TimeStampedModel):
    ACTIVE = 1
    GRADUATED = 2
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (GRADUATED, 'Graduated'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.academic_year_id:
            self.academic_year = AcademicYear.objects.get(is_active=True)
        return super().save(*args, **kwargs)


class Session(TimeStampedModel):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    period = models.IntegerField()
    date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.academic_year_id:
            self.academic_year = AcademicYear.objects.get(is_active=True)
        return super().save(*args, **kwargs)


class Attendance(TimeStampedModel):
    PENDING = 0
    PRESENT = 1
    ABSENT = 2
    LEAVE = 3
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LEAVE, 'Leave'),
    )

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)


class Assessment(TimeStampedModel):
    CHOICES = (
        ("sem written exam", "sem written Exam"),
        ("sem viva exam", "sem viva Exam"),

        ("internal exam", "Internal exam"),
        ("assignment", "Assignment"),
        ("project", "Project"),
        ("viva", "Viva"),
        ("seminar", "Seminar"),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.subject.name

    def save(self, *args, **kwargs):
        if not self.academic_year_id:
            self.academic_year = AcademicYear.objects.get(is_active=True)
        return super().save(*args, **kwargs)


class Grade(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
