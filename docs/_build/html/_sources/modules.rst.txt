QuizMe
======
..
   .. toctree::: This directive signals Sphinx to create a table of contents based on the listed documents
   :maxdepth: 4: This option specifies the maximum depth to which the table of contents will include sub-sections. 
   In this case, it's set to 4, meaning that sections up to four levels deep will be included in the table of contents.
   Django_website: The name of a document (a reStructuredText file) in your documentation project. 
   It represents a section or page within the documentation that you want to include in the table of contents. 
   Sphinx will automatically generate a link to this document in the table of contents.
   
   Add .rst files for each app to place automodules for each module (file) with a docstring, then place its name in the list

.. toctree::
   :maxdepth: 4

   QuizMe
   General_Knowledge
   Education
   Entertainment
   user_auth
