#!/usr/bin/env bash
#
# this is only run on a development machine!
#
cd ~/Devel/auctions
source ~/.virtualenvs/auctions/bin/activate
python manage.py test searching.tests.test_utils.DoSearchStoreResultsTests
