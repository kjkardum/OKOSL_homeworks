from app import app, db
from flask import render_template, jsonify  # , flash
from flask_user import login_required, roles_required, current_user
from .models import Homework, Task, Subtask, SolutionGroup, Remark  # , Solution, Remark
from .forms import RemarkForm, FinalRemarkForm
from .repository import Repository
# import datetime


NUMBER_OF_ARTICLES = 3


@app.route('/')
@app.route('/homeworks')
@login_required
def homeworks():
    years = sorted([homework.year for homework in Homework.query.distinct(Homework.year)])
    homeworks_by_year = {year: list(Homework.query.filter(Homework.year == year)) for year in years}
    return render_template('homeworks.html', years=years, homeworks_by_year=homeworks_by_year)


@app.route('/homeworks/<hw_id>')
@login_required
def homework(hw_id):
    homework = Homework.query.get(hw_id)
    return render_template('homework_page.html', homework=homework, Repository=Repository)


@app.route('/homeworks/<hw_id>/tasks/<task_id>')
@login_required
def task(task_id, hw_id):
    task = Task.query.get(task_id)
    homework = Homework.query.get(hw_id)
    return render_template('task_page.html', task=task, homework=homework)


@app.route('/homeworks/<hw_id>tasks/<task_id>/subtask_<subtask_id>')
@login_required
def subtask(subtask_id, task_id, hw_id):
    subtask = Subtask.query.get(subtask_id)
    task = Task.query.get(task_id)
    homework = Homework.query.get(task.homework_id)
    return render_template('subtask_page.html', subtask=subtask, task=task, homework=homework)


@app.route('/homeworks/<hw_id>tasks/<task_id>/subtask_<subtask_id>/solution_group_<solution_group_id>', methods=['GET', 'POST'])
@login_required
def solution_group(solution_group_id, subtask_id, task_id, hw_id):
    solution_group = SolutionGroup.query.get(solution_group_id)
    subtask = Subtask.query.get(subtask_id)
    task = Task.query.get(task_id)
    homework = Homework.query.get(hw_id)

    remark_form = RemarkForm()
    final_remark_form = FinalRemarkForm()
    author = current_user
    remark_added = False
    final_remark_added = False

    if remark_form.validate_on_submit() and remark_form.submit_remark.data:
        target_form = remark_form
        remark_added = True
    elif final_remark_form.validate_on_submit() and final_remark_form.submit_final_remark.data:
        target_form = final_remark_form
        final_remark_added = True

    if remark_added or final_remark_added:
        remark_text = target_form.remark_text.data
        remark_score_percentage = target_form.remark_score_percentage.data
        remark = Remark(author=author,
                        text=remark_text,
                        score_percentage=remark_score_percentage,
                        solution_group=solution_group
                        )

        if remark_added:
            db.session.add(remark)
            db.session.commit()
        else:
            if solution_group.final_remark is not None:
                db.session.delete(solution_group.final_remark)
            solution_group.final_remark = remark
            db.session.add(solution_group)
            db.session.commit()
    return render_template('solution_group_page.html',
                           remark_form=remark_form,
                           final_remark_form=final_remark_form,
                           solution_group=solution_group,
                           subtask=subtask,
                           task=task,
                           homework=homework
                           )


@app.route('/homeworks/<hw_id>/pull_solutions')
@login_required
def pull_solutions(hw_id):
    homework = Homework.query.get(hw_id)
    Repository.clone_n_parse(homework)
    return jsonify({'success': True})


@app.route('/homeworks/<hw_id>/push_remarks')
@login_required
def push_remarks(hw_id):
    homework = Homework.query.get(hw_id)
    # Repository.push_remarks(homework)
    print(f"Homework: {homework} - pushing remarks")
    return jsonify({'success': True})


@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return render_template('admin.html')
