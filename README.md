Heroku deployment url: https://gentle-fjord-99638.herokuapp.com/

Site admin 1:
username: admin1
password: bwa2018django1

Site admin 2:
username: admin2
password: bwa2018django2

Demo User : 
1. ariful3610@yahoo.com         Password : Ar661260
2. sazzad@oployeelabs.com       password: ZAQ!2wsx
3. biswa.jeet@gmail.com         password: ZAQ!2wsx
4. sazzad.rupak17@gmail.com     password: ZAQ!2wsx
5. asif.raihan@gmail.com        password: ZAQ!2wsx

## features
- [x] User
    - [x] Registration with mandatory information
        + real name
        + username
        + valid email address
        + phone number
        + address
        + date of birth
        + gender
        + image (can upload later)
    - [x] Login (Existing user)
    - [x] Logout (Existing user)
    - [x] Email validation on signup
    - [x] Reset forgotten password

- [x] User profile
    - [x] Add edit delete personal information
    - [x] show public data to everyone e.g. username, name
    - [x] show private data only to friends
    - [x] edit and save personal data
    - [x] add status message
    - [x] show latest message (including date and time of post) with chronological ordered comments first
    - [x] show previous message (including date and time of post) with chronological ordered comments

- [x] Friends, friend request information
    - [x] user can see his/her friends list (with link to friends' profile page)
    - [x] send friend request to second user
    - [x] First user can see the friend request given to second user
    - [x] Second user see the first users' friend request with username, name, date and time
    - [x] User can accept or reject the friend request came from other user
    - [x] User can see to whom they gave friend request and requests those came to the user (requests are those which has not been accepted or rejected yet)
    - [x] User can delete an existing friendship

- [x] Discussions
    - [x] User create a discussion (Let's say this user **"admin user"** for this discussion part)
    - [x] User can send text, see other users text under a discussion head (chronological order with date and time)
    - [x] User can edit and delete any text message, and a user can only delete his/her own comments
    - [x] Each Discussion should have a unique url and page
    
- [x] Notification
    - [x] User will get notification after 15 seconds
    - [x] Friend request incoming message, friend request accepted message, friend request withdrawn message, friend request delete message
    - [x] A Friend added a post status notification
    - [x] A friend added comment notification
    - [x] Every new discussion head notification created by friend
    - [x] New incoming text message notification
    
- [x] Search
    - [x] Main search (In the header)
        - [x] User can search by other user name, click user from result list and redirect to user profile page
        - [x] User can search by discussion header which are created by users' friends, can click on a discussion head and redirect it to discussion head view page
    
    - [x] Discussion search (In 'all discussion' view page )
        - [x] User can search by "user name", and the result will be those discussion heads where the "user name" added text
        - [x] User can search by a random "message text", and the result will be those discussion heads where the "message text" are found
    
    - [x] Discussion search (In a 'discussion head' view page )
        - [x] User can search by "user name", and the result will be those discussion heads where the "user name" added text
        - [x] User can search by a random "message text", and the result will be those lines where the "message text" are found
- [x] PostgreSQL database
- [x] 3rd party login


## Technological considerations
- [x] Django framework
- [x] Python as programming language
- [x] PostgreSQL database
- [x] HTML for template design
- [x] CSS
- [x] Bootstrap CSS faramework
- [x] JQuery
- [x] Font awesome icons
- [x] Ajax for discussion and feed loading
- [x] Heroku as deployment server


### Django apps in project

- [x] Normaluser App
- [x] Profile App
- [x] Friend App
- [x] Discussion App
- [x] Notification App

### Needed Django models and their attributes

- [x] Normal User Model
- [x] Friend Model
- [x] Discussion Model
- [x] Home Model
- [x] Notification Model
