Introduction
============

collective.pfg.payment extends PloneFormGen for payment use, so PloneFormGen needs to be installed.

For Verkkomakust S1
-------------------
From Site Setup, go to Payment Config

For testing input those values below to the each fields.

MAC Code:

6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ

Fields:

MERCHANT_ID
AMOUNT
ORDER_NUMBER
REFERENCE_NUMBER
ORDER_DESCRIPTION 
CURRENCY
RETURN_ADDRESS 
CANCEL_ADDRESS 
PENDING_ADDRESS 
NOTIFY_ADDRESS 
TYPE
CULTURE
PRESELECTED_METHOD 
MODE
VISIBLE_METHODS 
GROUP

Separator:

|

Capital:

Checked

Creat Start Form
----------------

Start Form is FormFolder where whole payment process starts.

Example Case
-------------
Donation Form
-------------

1. Create the first Form Folder

Under this Form Folder, add Decimal Number Form with id named AMOUNT.

2. Creat the socond Form Folder

Under this Form Folder, add String Fields with id named:

MERCHANT_ID
AMOUNT
ORDER_NUMBER
REFERENCE_NUMBER
ORDER_DESCRIPTION 
CURRENCY
RETURN_ADDRESS 
CANCEL_ADDRESS 
PENDING_ADDRESS 
NOTIFY_ADDRESS 
TYPE
CULTURE
PRESELECTED_METHOD 
MODE
VISIBLE_METHODS 
GROUP

Give default values for some fields:
--------------------------------------

MERCHANT_ID: 13466
CURERNCY: EUR
TYPE: S1
CULTURE: fi_FI
MODE: 1

Add another field : AUTHCODE
Go to overrides and input next:

python:here.restrictedTraverse('auth-code')


