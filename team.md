- We waited for Hayden's lecture to see if he was going to explain more about the project.

- After considering the tasks and files we need to work with, we set up tasks on the board, each task for each file i.e channel.py, auth.py. server.py. channels.py, etc.

- We gave a due date for each of us to select the files we are going to work with and for each person to take up reasonable load.

- In the first sprint, we focus on the implementation of functions assigned to each of us and discuss about the possible technical problems frequently on slack to make sure that everyone keeps up with the progress. 

- In the second sprint, we will complete the integration of the seperate parts and system test as well. Besides, if the time is sufficient enough, we will continue to exchange and review the codes among each other like what we do in it1.

- As we plan to have 2 sprints where the files will be passed to other team members for the second sprint, we set ourselves due date for Friday 20th March 2020.

    For sprint 1:

    Raymond: channel.py
    Sunny: message.py
    Dan: auth.py, user.py and server.py (in sprint 1, server.py is due on Mon, 23/3/2020)

- Other responsibilities such as implementing function decorator will be at first done individually and will be compiled as we approach finish.
    - Communication is required here as some function decorators are common between people. So as to not double up on work.
    - Everyone should guarantee that their code can run successfully with no errors before merge into the common branch.
    - Purpose of function decorators => authenticate, raise Exceptions. Changed the approach to function decorators from authenticating the entire function's parameters (e.g. @authenticate_login) to authenticating individual parameters for re-usability of function decorators (e.g. @authenticate_email, @authenticate_password).

- There are also files such as helper.py and data.json that we did not allocate originally but came up during progress. A team member usually volunteers to take responsiblity for these files although sometimes it may change.

- In our team Dan is responsible for helper.py which contain function decorator functions although some files may be done with individual style and may require some integration towards finish.


- Purpose of function decorators => authenticate, raise Exceptions. Changed the approach to function decorators from authenticating the entire function's parameters (e.g. @authenticate_login) to authenticating individual parameters for re-usability of function decorators (e.g. @authenticate_email, @authenticate_password).

- Raymond is responsible for common data file such as data.py and data.json. These files are also developed as we go and responsible person may change depending on need.
