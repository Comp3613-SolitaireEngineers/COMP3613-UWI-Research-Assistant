from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from.index import index_views
from App.controllers import *

author_views = Blueprint('author_views', __name__, template_folder='../templates')