from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Book
from . import db
import json
import requests
from llm_response import LLMResponse
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the OPENAI_KEY from environment variables
OPENAI_KEY = os.getenv("OPENAI_KEY")

views = Blueprint('views', __name__)

# model object
OPENAI_API = "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"
core = ChatOpenAI(
    openai_api_key=OPENAI_KEY,
    temperature=1.5,
    max_tokens=5000,
    model_name="gpt-4o-mini"
)

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
                journal = compile_journal(notes_data)
                gen_poem = generate_poem(journal)["poem"]
                gen_quote = json.dumps(generate_quotes(journal))

                
                 # store the JSON in book db
                new_book = Book(poem=gen_poem, quote=gen_quote, user_id=current_user.id)
                db.session.add(new_book)
                db.session.commit()

                # Use the mock response for now
                flash(f"Poem Generated Successfully", category='success')
                flash(f"Quote Generated Successfully", category='success')
            except Exception as e:
                # Handle request errors
                flash(f"Request failed: {e}", category='error')
         

    return render_template("home.html", user=current_user)


def compile_journal(notes):
    output_string = ""
    for note in notes:
        output_string += f"{note[0]}\n\n{note[1]}\n\n"
    return output_string

def generate_poem(journal):
    llm_response = LLMResponse(core, journal)
    poem = llm_response.poem_response()
    return poem
##

def generate_quotes(journal):
    llm_response = LLMResponse(core, journal)
    quote = llm_response.quote_response()
    return quote


@views.route('/popup_poem', methods=['GET'])
@login_required
def popup_poem():
    try:
        # Fetch the most recent poem for the current user
        poem_entry = (
            Book.query.filter_by(user_id=current_user.id)
            .filter(Book.poem.isnot(None))  # Ensure only entries with poems are fetched
            .order_by(Book.date.desc())  # Order by date in descending order
            .first()
        )

        if not poem_entry:
            raise ValueError("No poems found for the current user.")

        poem = poem_entry.poem
        return render_template('popup_poem.html', poem=poem)
    except Exception as e:
        return render_template('popup_poem.html', poem=f"Error: {e}")


@views.route('/popup_quote', methods=['GET'])
@login_required
def popup_quote():
    try:
        # Fetch the most recent quote for the current user
        quote_entry = (
            Book.query.filter_by(user_id=current_user.id)
            .filter(Book.quote.isnot(None))  # Ensure only entries with quotes are fetched
            .order_by(Book.date.desc())  # Order by date in descending order
            .first()
        )

        if not quote_entry:
            raise ValueError("No quotes found for the current user.")

        quote = quote_entry.quote
        return render_template('popup_quote.html', quote=quote)
    except Exception as e:
        return render_template('popup_quote.html', quote=f"Error: {e}")


@views.route('/popup_entry', methods=['GET'])
@login_required
def popup_entry():
    try:
        # Fetch all notes for the current user, sorted by date in descending order
        print(f"DEBUG: Current user ID: {current_user.id}")
        entries = (
            Note.query.filter_by(user_id=current_user.id)
            .order_by(Note.id.desc())
            .all()
        )

        # Debugging: Print raw entries from the database
        print("DEBUG: Raw entries fetched from the database:")
        for note in entries:
            print(f"ID: {note.id}, Data: {note.data}, Created At: {note.date}")


        # Prepare the entries in the format "date : entry"
        formatted_entries = [
            f"{note.date.strftime('%Y-%m-%d %H:%M:%S')} : {note.data}"
            for note in entries
        ]


        return render_template('popup_entry.html', entries=formatted_entries)
    except Exception as e:
        return render_template('popup_entry.html', entries=[], error=f"Error: {e}")


@views.route('/bookshelf', methods=['GET'])
@login_required
def bookshelf():
    return render_template("bookshelf.html", user=current_user)
