# AI WORKFLOW STUFF
Super Whisper: speech to text with LLM inference; holds right command;

When using /abcplan:
- Plan for the work
- Split it up so it can be done by agents in parallel
- Aggressively ask me questions
- Do the work on a worktree; ask which branch I should make that from
- Give me commands to copy and paste and open a new Cursor window

Nix for package/environment management.
- When you go into directory, it automatically attempts to activate the env!
- He doesn't have node global, so he does "direnv allow" to activate flake

He uses "make" for "MakeFile".
- This is essentially a sequence of shell commands
- Seems like a shell scripting process
- He keeps a global copy of all the .env files
    - These are like snippets of what's needed for each .env file
- Then using MakeFile script to stitch them together into THE .env
- Then he's using this so that it composes each of the .envs separately!!!
- So maybe he has 5 differnt types that it ultiately makes


Make personal software tools.


Firebase is what podverse is using for push notifications.
- Using it because it's the powerhouse standard for iOS/Android push notifications
- Meanwhile handrolled web browser push notification
- Firebase is like a mini AWS that's a suite of services? Maybe?
    - It's kind of like Google's version of a friendly AWS

He only uses PostGresSQL, just because that's what he knows.


So he says "Make the plans for the feature as separate markdown files,
assign the minimum needed model for each step of the of the plan,
then create a script that lets me create a worktree and move the
plan into it." The plans will be broken out into a 3 sections:
- 00-EXECUTION-ORDER.md is the summary of the plan
- 01-plan-runs-section.md and ++ how ever many mds it takes to do the mds
- COPY-PASTA.md is the commands he copy pastes into the command line
He runs this in the Cursor CLI. He wrote "/abconeatatime" which will take
questions from the CLI, and it will walk him through each question. It will
ultimately give him a command that will RESUME the CLI. So basically he has
another agent help him understand the error questions, come up answers, then
give him the answers to copy/paste back to the CLI.

Can't ask for "bulletproof"; instead ask for "confident" 


He uses SSE (server-sent events) so that he can play audio on different 
devices. 


Eval-Driven Development.



# REACT APP WORKFLOW STUFF

NextJS has an API server that you can use to write your own NodeJS backend.
Second option is anything else. Express is what Podverse uses.

The advantage of NextJS is, you can import functions directly to the frontend.
From the code perspective, they make it easy to call backend server endpoints
but without having to write out the full endpoint.

There is no "front end server". There's just the backend that serves up the
front end code to the client. Well, actually we need a front end that serves.
Maybe use "http-server"?
A "volume" for Docker container is term for storage;
it's mounted. You can mount that into a simple http-server on your container.

How do we get HTML buttons to interact with backend?
Button on-click event would send a HTTP request to the backend.

Forms: Unless you prevent it from doing so, if you press "enter", the form
interprets it as you want to submit it, but you can "prevent-default".
Different HTML tags have different behaviors across browsers.
AN INPUT WILL BE AN INPUT.

To load a React component from a FastAPI endpoint, you:
- Make the request for the data
- React has "state"; when you get the data from the server, you assign that
data to the state; whenever the state changes, then it will automatically
rebuild the DOM when needed.
- State is the bridge between the API data and the components.
- If you have the "count", it starts at 0. That can load by default.
    React knows that, when this "state" changes, we have to rerender these
    content;
- There's two states -- "count" and "is_loading". Is-loading is false by default.
    When user presses button, then is_loading. Are states like local fields?


- user presses button
- isLoading set to true
- loading spinner displays in the react component
- request to increment counter is sent to api
- server repllies after 10 second
- the response is received
- the count on the satate uses the response's count
- count on UI displays new count


Try to do a counter app in the morning that makes:
- React frontend
    - Actually, first do a CLI! Then Flask app! Then React app! All simultaneously!
    - Make the database shared across all. When you update CLI, it updates web!
- FastAPI backend
- Nginx, load balancer; traffic manager; web serving? Is it an HTTP server?
- Uses Docker containers on the server
- Setup observability with Honeycomb or Datadog
- ORM (could solve the "database interface stuff")
- IAM is "user-based permissions"; when you interact with Amazon Web Service
- Need to deploy to cloud!!! Deploy to AWS for experience.
- Should use different configurations for dev/debug and prod/release
- Integrate an external API... maybe send an email when counter hits 10?
    - Some browser notification tool?
- Use some kind of login system so only Derick can press the button!
- Make it run as both a CLI and Web using clean architecture.
- Use a mock during use_case testing to ensure no dependencies are needed!
- Use fixtures as factories in my testing suite, see tests/notes.md
- Use WorkOS to only allow myself to click the button, but everyone can view
- Redis and session data to keep track of darkmode / lightmode preferences
- Create a GPUI version desktop app?

i18n; when you make an application you can make it i18n
- this is "internationalization language"



