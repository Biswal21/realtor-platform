## Realtor  Platform

- [Realtor  Platform](#realtor-platform)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Status](#status)
  - [Contact](#contact)
  - [License](#license)

### Introduction

This is a platform for realtors to manage their properties and clients. It is a full stack application built with the Django Rest Framework, Postgres, Redis and Next.js stack.

### Features

- New user can register and login through phone number and OTP.
- User can look out for properties by narrowing down from city to region.
-  and search it based on builders in that region.
- User can view the details of the property and book a meeting based coupon with the realtor.
- They can reason for such booking of coupon for the property is to get a discount on the property from the commission for the realtor and brings in an assurance between client and seller.
- Client gets confirmation of the booking on their whatsapp number.
- Realtor can add properties and manage them through customised admin site of django.
- Realtor can add clients and manage them.

### Technologies

- Django Rest Framework
- Postgres
- Redis
- Next.js
- Tailwind CSS
- Docker
- Whatsapp Buisness API

### Setup

- Clone the repository
- Install Docker and Docker Compose

- Create a `.env` and `key.env` files in the root directory and add the following variables

- fill in the variable according to the example given in the `.env.example` and `key.env.example` files

 - Rune `docker-compose up --build` to build the containers and run the application.

### Usage

- The application will be running on `localhost:3000`
- The admin site will be running on `localhost:8000/admin`
- The api will be running on `localhost:8000/api/docs`

### Status

Project is: _intermediate stage_

- [x] User Authentication
- [x] Property Listing
- [x] Property Booking
- [x] Whatsapp Integration
- [x] Realtor Management
- [x] Client Management
- [x] Property Management
- [x] Payment Integration
- [x] Mobile browser layout
- [ ] Desktop browser layout
