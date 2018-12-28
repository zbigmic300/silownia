# Gym in Barbara dormitory #

## How do I get set up? ###
Install these python packages:  
    
    pip install -r requirements.txt 
    
## How to Dockerize an application? ###
    docker-compose build
    docker-compose up

### app should work in your host on http://localhost:4000/login
    
    

    
## Available API
### /login  
- file: resources/access_resource  
- class: LoginResource  
- POST  
  - description: login, get tokens  
  - request:  
    - login, type=str, required=True  
    - password, type=str, required=True  

### /logout  
- file: resources/access_resource  
- class: LogoutResource    
- POST  
  - description: logout, mark tokens revoked  
  - jwt: access_token  
  - request:  
    - refresh_token, type=str, required=True  

### /refresh  
- file: resources/access_resource  
- class: RefreshResource  
- POST  
  - description: refresh access token  
  - jwt: refresh_token  

### /changePassword  
- file: resources/password_resource  
- class: ChangePasswordResource  
- PATCH  
  - description: change user password  
  - jwt: access_token  
  - request:  
    - old_password, type=str, required=True  
    - new_password, type=str, required=True  

### /user  
- file: resources/user_resource  
- class: UserResource  
- GET  
  - description: get user data  
  - jwt: access_token  
- PUT  
  - description: modify user data  
  - jwt: access_token  
  - request:  
    - first_name, type=str, required=False  
    - last_name, type=str, required=False  
    - room, type=str, required=False  
- POST  
  - description: create new user application (user is inactive, need to be activated by admin)  
  - jwt: access_token  
  - request:    
    - login, type=str, required=True  
    - password, type=str, required=True  
    - first_name, type=str, required=False  
    - last_name, type=str, required=False  
    - room, type=str, required=False  

### /admin/users  
- file: resources/admin_resource  
- class: AdminUsersResource  
- admin: required  
- GET  
  - description: get user list with filtering  
  - jwt: access_token  
  - request:  
    - login, type=str, required=False  
    - admin, type=bool, required=False  
    - first_name, type=str, required=False  
    - last_name, type=str, required=False  
    - room, type=str, required=False  
    - status, type=str, required=False  
    - order, type=str, required=False  
    - descending, type=bool, required=False  
- POST  
  - description: create new active user  
  - jwt: access_token  
  - request:  
    - login, type=str, required=True  
    - password, type=str, required=True  
    - admin, type=bool, required=False  
    - first_name, type=str, required=False  
    - last_name, type=str, required=False  
    - room, type=str, required=False  

### /admin/user/user_id  
- file: resources/admin_resource  
- class: AdminUserResource  
- admin: required  
- parameter: user_id - id of user  
- GET  
  - description: get data of user  
  - jwt: access_token  
- PUT  
  - description: modify data of user  
  - jwt: access_token  
  - request:  
    - admin, type=bool, required=False  
    - first_name, type=str, required=False  
    - last_name, type=str, required=False  
    - room, type=str, required=False  
- PATCH  
  - description: activate user (change status to A)  
  - jwt: access_token  
- DELETE  
  - description: remove user  
  - jwt: access_token  

### /reservation/reservation_id  
- file: resources/reservation_resource  
- class: ReservationResource  
- parameter: reservation_id - id of reservation  
- GET  
  - description: get reservation data  
  - jwt: access_token  
- DELETE  
  - description: remove reservation  
  - jwt: access_token  

### /reservations  
- file: resources/reservation_resource  
- class: ReservationsResource  
- parameter: user_id - id of user  
- GET  
  - description: get user's reservations  
  - jwt: access_token  
- POST  
  - description: create new reservation  
  - jwt: access_token  
  - request:  
    - start_date, type=date with format (%Y-%m-%dT%H:%M:%S), required=True  
    - end_date, type=date with format (%Y-%m-%dT%H:%M:%S), required=True  

### /week/reservations  
- file: resources/reservation_resource  
- class: WeekReservationsResource  
- GET  
  - description: get this weeks reservations  
  - jwt: access_token  
