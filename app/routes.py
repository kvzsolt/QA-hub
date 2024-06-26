from flask import Blueprint
from . import views

routes_blueprint = Blueprint("routes", __name__)

routes_blueprint.route("/", methods=["GET"])(views.main_page)
routes_blueprint.route("/list", methods=["GET", "POST"])(views.route_list)
routes_blueprint.route("/question/<question_id>", methods=["GET", "POST"])(views.route_question_id)
routes_blueprint.route("/add-question", methods=["GET", "POST"])(views.route_add_question)
routes_blueprint.route("/question/<question_id>/delete", methods=["POST"])(views.route_delete_question)
routes_blueprint.route("/question/<question_id>/edit-question", methods=["GET", "POST"])(views.route_edit_question)
routes_blueprint.route("/question/<question_id>/new-answer", methods=["GET", "POST"])(views.add_new_answer)
routes_blueprint.route("/answer/<answer_id>/delete", methods=["GET", "POST"])(views.delete_answer)
routes_blueprint.route("/question/<question_id>/vote")(views.route_question_votes)
routes_blueprint.route("/answer/<answer_id>/vote")(views.answer_vote)
routes_blueprint.route("/question/<question_id>/new_comment", methods=["GET", "POST"])(views.add_new_question_comment)
routes_blueprint.route("/answer/<answer_id>/new_comment", methods=["POST"])(views.add_new_answers_comment)
routes_blueprint.route("/answer/<answer_id>/edit", methods=["GET", "POST"])(views.edit_answer)
routes_blueprint.route("/comments/<comment_id>/delete", methods=["POST"])(views.question_comment_delete)
routes_blueprint.route("/answer_comments/<comment_id>/delete", methods=["POST"])(views.answer_comment_delete)
routes_blueprint.route("/login", methods=["GET", "POST"])(views.login)
routes_blueprint.route("/logout", methods=["GET"])(views.logout)
routes_blueprint.route("/register", methods=["GET", "POST"])(views.register)
routes_blueprint.route("/users", methods=["GET", "POST"])(views.users_list)
routes_blueprint.route("/user/<user_id>", methods=["GET"])(views.specific_user_questions)
routes_blueprint.route("/question/<question_id>/new-tag", methods=["GET", "POST"])(views.add_tag)
routes_blueprint.route("/question/<question_id>/tag/<tag_id>/delete")(views.delete_tag)
routes_blueprint.route("/tags", methods=["GET"])(views.list_tags)
routes_blueprint.route("/answer-vote/<int:answer_id>/<int:data>", methods=["GET", "POST"])(views.accept_answer)
