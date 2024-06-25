from datetime import datetime

from sqlalchemy import func

from .forms import LoginForm, RegistrationForm, QuestionForm, TagForm, \
    EditAnswerForm, EditQuestionForm
from markupsafe import escape
from flask import render_template, request, url_for, redirect, session
from . import db, utils
from .models import User, Question, Answer, Comment, Tag, QuestionTag

ROUTE_LIST_PAGE = "/list"


def main_page():
    first_five_question = Question.query.order_by(Question.submission_time.desc()).limit(5).all()
    return render_template('main.html', first_five_question=first_five_question)


def route_list():
    search = request.args.get('search')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    if search:
        questions = Question.query.filter(Question.title.ilike(f'%{search}%')).order_by(Question.id).all()
    elif order_by:
        questions = Question.query.order_by(db.text(f'{order_by} {order_direction}')).all()
    else:
        questions = Question.query.order_by(Question.id).all()

    log = None
    id_value = None
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            id_value = user.id
            log = escape(session['email'])

    return render_template("list_questions.html", questions=questions, id_value=id_value, log=log, search_phrase=search)


def route_question_id(question_id):
    question = Question.query.get(question_id)
    answers = Answer.query.filter_by(question_id=question_id).order_by(Answer.id).all()
    tags = Tag.query.join(QuestionTag).filter(QuestionTag.question_id == question_id).all()
    comments = Comment.query.filter_by(question_id=question_id).all()
    answer_comments = Comment.query.all()
    is_answer_accepted = answers[0].is_answer_accepted if answers else 0

    if request.method == 'GET':
        question.view_number += 1
        db.session.commit()

    return render_template("question(_and_answers).html", question=question, answers=answers, comments=comments,
                           answer_comments=answer_comments, is_answer_accepted=is_answer_accepted, tags=tags)


def route_add_question():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        if 'email' in session:
            email = session['email']
            user = User.query.filter_by(email=email).first()
            if user:
                new_question = Question(
                    title=form.title.data,
                    message=form.message.data,
                    image=form.image.data.read() if form.image.data else None,
                    user_id=user.id,
                    submission_time=datetime.now(),
                    view_number=0,
                    vote_number=0
                )
                db.session.add(new_question)
                db.session.commit()
                return redirect(url_for('route_list'))
        else:
            return redirect(url_for('login'))
    return render_template('add_question.html', form=form)


def route_delete_question(question_id):
    Question.query.filter_by(id=question_id).delete()
    db.session.commit()
    return redirect('/')


def route_edit_question(question_id):
    question = Question.query.get(question_id)
    form = EditQuestionForm(obj=question)

    if request.method == 'POST' and form.validate_on_submit():
        question.title = form.title.data
        question.message = form.message.data
        if form.image.data:
            question.image = form.image.data.read()
        db.session.commit()
        return redirect(url_for('route_question_id', question_id=question_id))

    return render_template('edit_question.html', form=form, question=question)


def add_new_answer(question_id):
    if request.method == "GET":
        question = Question.query.get(question_id)
        return render_template("add_answer.html", question=question)
    elif request.method == "POST":
        if "email" in session:
            email = session["email"]
            user = User.query.filter_by(email=email).first()
            if user:
                answer = Answer(
                    question_id=question_id,
                    message=request.form['message'],
                    image=request.form.get('image'),
                    user_id=user.id,
                    submission_time=datetime.now(),
                    vote_number=0,
                    is_answer_accepted=0
                )
                db.session.add(answer)
                db.session.commit()
        return redirect(f'/question/{question_id}')


def delete_answer(answer_id):
    answer = Answer.query.get(answer_id)
    if answer:
        question_id = answer.question_id
        Answer.query.filter_by(id=answer_id).delete()
        db.session.commit()
        return redirect(f"/question/{question_id}")
    return redirect('/')


def route_question_votes(question_id):
    vote = request.args.get('vote')
    user_id = request.args.get('user_id')
    question = Question.query.get(question_id)
    if question:
        question.vote_number += 1 if vote == '+' else -1
        db.session.commit()

        reputation = 5 if vote == '+' else -2
        user = User.query.get(user_id)
        if user:
            user.reputation += reputation
            db.session.commit()
    return redirect(ROUTE_LIST_PAGE)


def answer_vote(answer_id):
    vote = request.args.get('vote')
    user_id = request.args.get('user_id')
    answer = Answer.query.get(answer_id)
    if answer:
        answer.vote_number += 1 if vote == '+' else -1
        db.session.commit()

        reputation = 10 if vote == '+' else -2
        user = User.query.get(user_id)
        if user:
            user.reputation += reputation
            db.session.commit()
        return redirect(f"/question/{answer.question_id}")
    return redirect('/')


def add_new_question_comment(question_id):
    if request.method == 'POST':
        new_comment = request.form['message']
        if "email" in session:
            email = session["email"]
            user = User.query.filter_by(email=email).first()
            if user:
                comment = Comment(
                    question_id=question_id,
                    message=new_comment,
                    submission_time=datetime.now(),
                    user_id=user.id
                )
                db.session.add(comment)
                db.session.commit()
        return redirect(f'/question/{question_id}')
    return redirect(f'/question/{question_id}')


def add_new_answers_comment(answer_id):
    new_comment = request.form['add_comment_message']
    answer = Answer.query.get(answer_id)
    if answer:
        question_id = answer.question_id
        if "email" in session:
            email = session["email"]
            user = User.query.filter_by(email=email).first()
            if user:
                comment = Comment(
                    answer_id=answer_id,
                    message=new_comment,
                    submission_time=datetime.now(),
                    user_id=user.id
                )
                db.session.add(comment)
                db.session.commit()
        return redirect(f'/question/{question_id}')
    return redirect('/')


def edit_answer(answer_id):
    answer = Answer.query.get(answer_id)
    form = EditAnswerForm(obj=answer)

    if request.method == 'POST' and form.validate_on_submit():
        answer.message = form.message.data
        if form.image.data:
            answer.image = form.image.data.read()
        db.session.commit()
        return redirect(url_for('route_question_id', question_id=answer.question_id))

    return render_template('edit_answer.html', form=form, answer=answer)


def question_comment_delete(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        question_id = comment.question_id
        Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()
        return redirect(f'/question/{question_id}')
    return redirect('/')


def answer_comment_delete(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        answer = Answer.query.get(comment.answer_id)
        if answer:
            question_id = answer.question_id
            Comment.query.filter_by(id=comment_id).delete()
            db.session.commit()
            return redirect(f'/question/{question_id}')
    return redirect('/')


def login():
    form = LoginForm()
    error_message = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and utils.verify_password(password, user.password):
            session['email'] = email
            session['user_id'] = user.id
            return redirect(url_for('route_list'))
        else:
            error_message = "Invalid username or password!"
    return render_template('login.html', form=form, error_message=error_message)


def logout():
    session.pop('email', None)
    return redirect(url_for('route_list'))


def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = utils.hash_password(form.password.data)
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['email'] = email
        session['user_id'] = user.id
        return redirect(url_for('routes.route_list'))
    return render_template('register.html', form=form)


def users_list():
    users = User.query.all()
    return render_template('users.html', users=users)


def specific_user_questions(user_id):
    user = User.query.get(user_id)
    questions = Question.query.filter_by(user_id=user_id).all()
    answers = Answer.query.filter_by(user_id=user_id).all()
    comments = Comment.query.filter_by(user_id=user_id).all()
    return render_template('user_specific_questions.html', user=user, questions=questions, answers=answers, comments=comments)


def add_tag(question_id):
    form = TagForm()
    question = Question.query.get(question_id)
    tags = Tag.query.all()
    form.existing_tag.choices = [(tag.id, tag.name) for tag in tags]

    if request.method == 'POST' and form.validate_on_submit():
        tag_id = None
        if form.new_tag.data:
            new_tag = Tag(name=form.new_tag.data)
            db.session.add(new_tag)
            db.session.commit()
            tag_id = new_tag.id
        else:
            tag_id = form.existing_tag.data

        if tag_id:
            question_tag = QuestionTag(question_id=question_id, tag_id=tag_id)
            db.session.add(question_tag)
            db.session.commit()
        return redirect(url_for('route_question_id', question_id=question_id))

    return render_template('add_tag.html', form=form, question=question)


def delete_tag(question_id, tag_id):
    QuestionTag.query.filter_by(question_id=question_id, tag_id=tag_id).delete()
    db.session.commit()
    return redirect(f'/question/{question_id}')


def list_tags():
    tags = db.session.query(
        Tag.name,
        func.count(Tag.id).label('num_of_use')
    ).join(QuestionTag).group_by(Tag.id).all()
    return render_template('tag_page.html', tags=tags)


def accept_answer(answer_id, data):
    user_email = session.get('email')
    if user_email:
        answer = Answer.query.get(answer_id)
        if answer:
            question_id = answer.question_id
            question = Question.query.get(question_id)
            user = User.query.filter_by(email=user_email).first()
            if question.user_id == user.id:
                answer.is_answer_accepted = data
                db.session.commit()
                reputation = 15 if data == 1 else -15
                answer_user = User.query.get(answer.user_id)
                answer_user.reputation += reputation
                db.session.commit()
                return redirect(f'/question/{question_id}')
    return redirect('/')
