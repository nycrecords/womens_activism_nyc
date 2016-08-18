"""
.. module:: utils.

   :synopsis: Utiltiy functions used throughout the application.
"""

flag_choices = [('Inappropriate Content', 'Inappropriate Content'),
                ('Offensive Content', "Offensive Content"),
                ('Wrong Information', 'Wrong Information'),
                ('Other', 'Other')]

archive_tags = ['Abolitionists',
                'Africa',
                'Antarctica',
                'Arts and Entertainment',
                'Asia',
                'Australia',
                'Business and Entrepreneurship',
                'Civil and Human Rights',
                'Education',
                'Environment',
                'Europe',
                'Government and Politics',
                'Health',
                'LGBTQ',
                'Law',
                'Literature',
                'Military',
                'North America',
                'Religion',
                'Science, Technology, Engineering and Math (STEM)',
                'South America',
                'Sports',
                'Suffrage']



class InvalidResetToken(Exception):
    pass