"""
.. module:: utils.

   :synopsis: Utiltiy functions used throughout the application.
"""

flag_choices = [('Inappropriate Content', 'Inappropriate Content'),
                ('Offensive Content', "Offensive Content"),
                ('Wrong Information', 'Wrong Information'),
                ('Other', 'Other')]

archive_tags = ['Abolition',
                'Arts and Entertainment',
                'Business and Entrepreneurship',
                'Civil and Human Rights',
                'Education',
                'Environment',
                'Government and Politics',
                'Health',
                'LGBTQ',
                'Law',
                'Literature and Journalism',
                'Military',
                'Religion',
                'Science, Technology, Engineering, and Math (STEM)',
                'Sports',
                'Suffrage',
                'Other']



class InvalidResetToken(Exception):
    pass