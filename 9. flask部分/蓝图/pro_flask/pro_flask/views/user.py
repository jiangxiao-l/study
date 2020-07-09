#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template
user = Blueprint('user', __name__)

@user.route('/login.html', methods=['GET', "POST"])
def login():

