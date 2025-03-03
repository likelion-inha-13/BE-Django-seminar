from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager): # 일반 사용자 & 관리자 계정 생성
    def create_user(self, user_id, email, name, generation, gender, password=None):
        # 이메일과 이름을 받아 User 객체 생성
        user = self.model(
            user_id= user_id,
            email=self.normalize_email(email),
            name=name,
            generation = generation,
            gender = gender,
        )

        user.set_password(password) # 비밀번호 해싱 처리
        user.save(using=self._db) # DB에 저장
        return user

    def create_superuser(self, user_id, email, name, generation, gender, password):
        # 일반 유저 생성 후 is_admin = True로 관리자 계정 생성
        user = self.create_user(
            user_id= user_id,
            email=email,
            name=name,
            generation=generation,
            gender=gender,
            password=password,
        )

        user.is_admin = True # 관리자 권한 부여
        user.save(using=self._db)
        return user


class User(AbstractBaseUser): # AbstractBaseUser를 상속하여 User 모델 커스텀
    user_id = models.CharField(
        verbose_name='user_id',
        max_length=30,
        unique=True, # 아이디는 고유해야 함
    )

    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        unique=True, # 이메일은 고유해야 함
    )
    name = models.CharField(max_length=30)
    generation = models.PositiveIntegerField(verbose_name="멋사기수") # 기수는 양수만 허용


    GENDER_OPT =(
        ('남', '남자'),
        ('여', '여자'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_OPT, default='')
    is_active = models.BooleanField(default=True) # 계정 활성화 여부
    is_admin = models.BooleanField(default=False) # 관리자 여부 (처음 생성시 false)

    objects = UserManager() # 기본 UserManager 대신 커스텀 UserManager(우리가 커스텀 한 class) 사용

    USERNAME_FIELD = 'user_id' # 로그인 시 user_id를 ID로 사용
    # 기본 User 모델은 username을 사용하지만 우리(실습시간)는 email로

    REQUIRED_FIELDS = ['email', 'name', 'generation', 'gender'] # 'createsuperuser' 실행 시 입력해야 할 필드

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True # 모든 권한 허용 (추후 수정 가능)

    def has_module_perms(self, app_label):
        return True # 모든 앱에 접근 가능 (추후 수정 가능)

    @property
    def is_staff(self): # is_admin이 True이면 is_staff도 True로 설정
        return self.is_admin
    
    class Meta:
        db_table = 'user' # 테이블명을 user로 설정