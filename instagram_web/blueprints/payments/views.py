from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
import os
import braintree
from helpers.helpers import gateway, find_transaction, transact, TRANSACTION_SUCCESS_STATUSES, generate_client_token
from helpers.sendgrid import deliver_mail
from models.donations import Donations
from models.post import Post

payments_blueprint = Blueprint('payments',
                               __name__,
                               template_folder='templates')


@payments_blueprint.route('/<post_id>/new', methods=['GET'])
def new_checkout(post_id):
    post = Post.get_or_none(id=post_id)
    client_token = generate_client_token()
    return render_template('payments/new.html', post=post, client_token=client_token)

@payments_blueprint.route('/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('payments/show.html', transaction=transaction, result=result)

@payments_blueprint.route('/<post_id>/checkouts', methods=['POST'])
def create_checkout(post_id):
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        user_id = current_user.id
        amount = request.form.get('amount')
        post_id = Post.get(Post.user_id == user_id)
        Donations.create(amount=amount, user_id=current_user.id, post_id=post_id)
        deliver_mail()
        return redirect(url_for('payments.show_checkout', transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('payments.new_checkout', post_id=post_id))