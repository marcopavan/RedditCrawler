#!/usr/bin/python
# -*- coding: utf-8 -*-

# USAGE EXAMPLE:
# to get top submissions:
# python crawler.py -t -v
# or to get hot submissions:
# python crawler.py -l -v
# or to get a single submissions:
# python crawler.py -s id -v


import argparse
import praw
import csv
import codecs
import time
from functions import *
import sys


parser = argparse.ArgumentParser(description='Debug')
parser.add_argument("-n", metavar='id', help="Insert submission id")
parser.add_argument("-t", action="store_true", help="get top submissions")
parser.add_argument("-s", action="store_true", help="get hot submissions")
parser.add_argument("-l", default="1", help="Limit the number of retrieved conversations (only used with conversation keywords like 'hot' or 'top')")
parser.add_argument("-v", action="store_true", help="Verbose mode for logging")
args = parser.parse_args()

# Authenticate
user_agent = 'Script for retrieving comments'
r = praw.Reddit(user_agent=user_agent)

# get top post

# Time for the whole submissions
start_tot_time = int(round(time.time() * 1000))

# if args.v:
#     print "Fetching submissions..."

if args.t or args.s:
    if args.t:
        # Get top submissions
        top_posts = r.get_subreddit('all').get_top_from_all(limit=int(args.l))

    elif args.s:
        # Get hot submissions
        top_posts = r.get_subreddit('all').get_hot(limit=int(args.l))

    i = 1
    for p in top_posts:
        # Time for 1 submission
        start_sub_time = int(round(time.time() * 1000))

        # Open csv file for every submission
        csv_output = codecs.open('Datasets/'+"%s_%s.csv" % (str(p.subreddit.display_name), str(p.id)), "w",
                                encoding='utf-8')
        wr = csv.writer(csv_output)
        # Write categories on csv
        wr.writerow(['Comment Id', 'Author ID', 'Text', 'HasReplies', 'RepliesTo', 'Score', 'Author Comment Karma', 'Author Link Karma'])

        if args.v:
            print "Getting submission " + str(i) + "/" + str(args.l) +"..."

        has_replies = False
        # Get Author
        try:
            author = str(p.author.name)
        except:
            author = "None"
        # Get Author Comment e Link Karma
        try:
            user1 = r.get_redditor(author)
        except:
            user1 = None
        try:
            user1_l_karma = user1.link_karma
        except:
            user1_l_karma = None
        try:
            user1_c_karma = user1.comment_karma
        except:
            user1_c_karma = None
        # Get Submission title
        submission_text = str(sanitize(p.title))
        # Get Submission text
        self_text = str(sanitize(p.selftext))
        # Get submission Id
        submission_id = str(p.id)
        # Get submission score
        submission_score = str(p.score)

        # Control if submission has replies
        if len(p.comments) == 0:
            has_replies = False

        # Write submission on csv
        wr.writerow(
            [submission_id, author, submission_text + " " + self_text, has_replies, "",
                submission_score, user1_c_karma, user1_l_karma])

        # Change value MoreComments to list of Comments
        p.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(p.comments)

        comment_count = 1
        # Scan comments list
        for c in flat_comments:

            if args.v:
                # print"Getting comment " + str(comment_count) + "/" + str(len(flat_comments))
                message = "Comment extracted " + str(comment_count) + "/" + str(len(flat_comments))
                if comment_count==len(flat_comments):
                    sys.stdout.write("%s \n"%(message))
                else:
                    sys.stdout.write("%s \r"%(message))
                sys.stdout.flush()

            if c.parent_id != None:
                has_replies = True

            # Get comment Id
            comment_id = str(c.id)
            # Get comment author
            try:
                comment_author = str(c.author)
            except:
                comment_author = "None"
            # Get Author Comment e Link Karma
            try:
                user2 = r.get_redditor(author)
            except:
                user2 = None
            try:
                user2_l_karma = user2.link_karma
            except:
                user2_l_karma = None
            try:
                user2_c_karma = user1.comment_karma
            except:
                user2_c_karma = None
            # Get comment text
            comment_text = str(sanitize(c.body))
            # Get comment score
            comment_score = str(c.score)
            # Get id in reply to
            comment_in_reply_to_id = str(c.parent_id)

            if len(c.replies) == 0:
                has_replies = False

            # Check if comment/author is valid
            if comment_text.find('[deleted]') == -1 or comment_author.find('None') == -1 or comment_author.find('[removed]') == -1:
                # Write comment in csv file
                wr.writerow([comment_id, comment_author, comment_text, has_replies,
                            replyId_cleaner(comment_in_reply_to_id),
                            comment_score, user2_c_karma, user2_l_karma])
            comment_count += 1

        csv_output.close()
        end_sub_time = int(round(time.time() * 1000))
        if args.v:
            print "Finished retrieving submission " + str(i) + "/" + str(args.l)
            printTime(start_sub_time, end_sub_time)
        i += 1

    end_tot_time = int(round(time.time() * 1000))

    if args.v:
        print "Finished retrieving submissions"
        printTime(start_tot_time, end_tot_time)


elif args.n:
    # Getting submission from id
    submission = r.get_submission(submission_id=str(args.n))

    # Open csv file for every submission
    csv_output = codecs.open('Datasets/'+"%s_%s.csv" % (str(submission.subreddit.display_name), str(submission.id)), "w",
                            encoding='utf-8')
    wr = csv.writer(csv_output)
    # Write categories on csv
    wr.writerow(['Comment Id', 'Author ID', 'Text', 'HasReplies', 'RepliesTo', 'Score', 'Author Comment Karma', 'Author Link Karma'])

    if args.v:
        print "Getting submission..."

    has_replies = False
    # Get Author
    try:
        author = str(submission.author.name)
    except:
        author = "None"
    # Get Author Comment e Link Karma
    try:
        user1 = r.get_redditor(author)
    except:
        user1 = None
    try:
        user1_l_karma = user1.link_karma
    except:
        user1_l_karma = None
    try:
        user1_c_karma = user1.comment_karma
    except:
        user1_c_karma = None
    # Get Submission title
    submission_text = str(sanitize(submission.title))
    # Get Submission text
    self_text = str(sanitize(submission.selftext))
    # Get submission Id
    submission_id = str(submission.id)
    # Get submission score
    submission_score = str(submission.score)

    # Control if submission has replies
    if len(submission.comments) == 0:
        has_replies = False

    # Write submission on csv
    wr.writerow(
        [submission_id, author, submission_text + " " + self_text, has_replies, "",
            submission_score, user1_c_karma, user1_l_karma])

    # Change value MoreComments to list of Comments
    submission.replace_more_comments(limit=None, threshold=0)
    flat_comments = praw.helpers.flatten_tree(submission.comments)

    comment_count = 1
    # Scan comments list
    for c in flat_comments:

        if args.v:
            # print "Getting comment " + str(comment_count) + "/" + str(len(flat_comments))
            message = "Comment extracted " + str(comment_count) + "/" + str(len(flat_comments))
            if comment_count==len(flat_comments):
                sys.stdout.write("%s \n"%(message))
            else:
                sys.stdout.write("%s \r"%(message))
            sys.stdout.flush()

        if c.parent_id != None:
            has_replies = True

        # Get comment Id
        comment_id = str(c.id)
        # Get comment author
        try:
            comment_author = str(c.author)
        except:
            comment_author = "None"
        # Get Author Comment e Link Karma
        try:
            user2 = r.get_redditor(author)
        except:
            user2 = None
        try:
            user2_l_karma = user2.link_karma
        except:
            user2_l_karma = None
        try:
            user2_c_karma = user1.comment_karma
        except:
            user2_c_karma = None
        # Get comment text
        comment_text = str(sanitize(c.body))
        # Get comment score
        comment_score = str(c.score)
        # Get id in reply to
        comment_in_reply_to_id = str(c.parent_id)
        comment_count += 1

        if len(c.replies) == 0:
            has_replies = False

        # Check if comment/author is valid
        if comment_text.find('[deleted]') == -1 or comment_author.find('None') == -1 or comment_author.find('[removed]') == -1:
            # Write comment in csv file
            wr.writerow([comment_id, comment_author, comment_text, has_replies,
                        replyId_cleaner(comment_in_reply_to_id),
                        comment_score, user2_c_karma, user2_l_karma])

    csv_output.close()
    end_tot_time = int(round(time.time() * 1000))

    if args.v:
        print "Finished retrieving submissions"
        printTime(start_tot_time, end_tot_time)
