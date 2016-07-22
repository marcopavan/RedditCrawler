#!/usr/bin/env python
# -*- coding: utf-8 -*-

class RedditText(object):

	def __init__(self,
				commentId,authorId,text,hasReplies,repliesTo,score,commentKarma,linkKarma):
		self.id = commentId
		self.authorId = authorId
		self.text = text
		self.hasReplies = hasReplies
		self.repliesTo = repliesTo			# textID to attack
		self.score = score
		self.commentKarma = commentKarma
		self.linkKarma = linkKarma