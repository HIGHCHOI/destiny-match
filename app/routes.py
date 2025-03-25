from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import register_user, get_user_by_email, get_user_by_id, update_profile
from passlib.hash import pbkdf2_sha256
from app.models import get_user_by_id, get_all_users_except
from app.recommend_utils import (
    age_similarity,
    mbti_similarity,
    hobbies_similarity,
    music_similarity,
    ideal_match
)


bp = Blueprint('bp', __name__)

@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('bp.profile'))
    return render_template('index.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        try:
            register_user(email, username, password)
            flash('회원가입 성공! 로그인 해주세요.', 'success')
            return redirect(url_for('bp.index'))
        except Exception as e:
            flash(f'회원가입 실패: {e}', 'danger')
    return render_template('signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and pbkdf2_sha256.verify(password, user['password']):
            session['user_id'] = user['id']
            return redirect(url_for('bp.profile'))
        else:
            flash("이메일 또는 비밀번호가 잘못되었습니다.", 'danger')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("로그아웃 되었습니다.", 'info')
    return redirect(url_for('bp.index'))

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('bp.login'))

    user = get_user_by_id(user_id)

    if request.method == 'POST':
        update_profile(
            user_id,
            request.form['name'],
            request.form['age'],
            request.form['gender'],
            request.form['mbti'],
            request.form['hobbies'],
            request.form['music_style'],
            request.form['height'],
            request.form['weight'],
            request.form['personality'],
            request.form['appearance'],
            request.form['body_shape'],
            request.form['ideal_age_diff'],
            request.form['ideal_mbti'],
            request.form['ideal_personality'],
            request.form['ideal_appearance'],
            request.form['ideal_height_range'],
            request.form['ideal_weight_range'],
            request.form['ideal_body_shape']
        )


        flash("프로필이 저장되었습니다.", 'success')
        return redirect(url_for('bp.profile'))

    return render_template('profile.html', user=user)

@bp.route('/recommend')
def recommend():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('bp.login'))

    current_user = get_user_by_id(user_id)
    all_users = get_all_users_except(user_id)

    # 추천 결과 계산
    age_sim = age_similarity(current_user, all_users)
    mbti_sim = mbti_similarity(current_user, all_users)
    hobby_sim = hobbies_similarity(current_user, all_users)
    music_sim = music_similarity(current_user, all_users)
    ideal_sim = ideal_match(current_user, all_users)

    return render_template(
        "recommend.html",
        user=current_user,
        age_sim=age_sim,
        mbti_sim=mbti_sim,
        hobby_sim=hobby_sim,
        music_sim=music_sim,
        ideal_sim=ideal_sim
    )
