from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import requests

views = Blueprint('views', __name__)
API_URL = "https://henry'surl.com/generate" 


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Get the note from the form

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # Save the note to the database
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

            # Fetch the last 10 notes added by the current user
            last_10_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.id.desc()).limit(10).all()

            # Extract the data from the notes
            notes_data = [note.data for note in last_10_notes]

            # Send a POST request to your friend's API
     
            try:
                #response = requests.post(API_URL, json={"notes": notes_data})
                #if response.status_code == 200:
                    # API call was successful
                #    result = response.json()
                #    flash(f"Generated Poem: {result.get('poem', 'No poem received')}", category='success')
                #    flash(f"Generated Quote: {result.get('quote', 'No quote received')}", category='success')
                #else:
                    # Handle API errors
                #  flash(f"API Error: {response.status_code} - {response.text}", category='error')
                mock_response = {
                    "poem": "a is a b is b and c is s",
                    "quote": "this is the most amazing poem ever"
                }
                # Use the mock response for now
                flash(f"Generated Poem: {mock_response.get('poem')}", category='success')
                flash(f"Generated Quote: {mock_response.get('quote')}", category='success')
            except Exception as e:
                # Handle request errors
                flash(f"Request failed: {e}", category='error')
         

    return render_template("home.html", user=current_user)


@views.route('/popup_poem', methods=['GET'])
@login_required
def popup_poem():
    # Mock response as placeholder
    # Replace this section with the actual API call when ready
    try:
        # Uncomment when API is ready
        # response = requests.get(API_POEM_URL, timeout=5)
        # if response.status_code == 200:
        #     poem = response.json().get('poem', 'No poem available.')
        # else:
        #     poem = "Failed to fetch poem from API."
        
        # Mock data for now
        poem = "This is a placeholder poem about life and beauty."
        return render_template('popup_poem.html', poem=poem)
    except Exception as e:
        return render_template('popup_poem.html', poem=f"Error: {e}")


@views.route('/popup_quote', methods=['GET'])
@login_required
def popup_quote():
    # Mock response as placeholder
    # Replace this section with the actual API call when ready
    try:
        # Uncomment when API is ready
        # response = requests.get(API_QUOTE_URL, timeout=5)
        # if response.status_code == 200:
        #     quote = response.json().get('quote', 'No quote available.')
        # else:
        #     quote = "Failed to fetch quote from API."

        # Mock data for now
        quote = "This is a placeholder quote: 'To be or not to be.'"
        return render_template('popup_quote.html', quote=quote)
    except Exception as e:
        return render_template('popup_quote.html', quote=f"Error: {e}")

@views.route('/bookshelf', methods=['GET'])
@login_required
def bookshelf():
    return render_template("bookshelf.html", user=current_user)
