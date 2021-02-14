# Sezzle Web API Technical Test

Welcome to my take on the Sezzle Web API test!

## How To Use This API

Whomever is evaluating my API will have the link to where this is hosted, but otherwise, interacting with my API is pretty simple; there are 4 REST commands to interact with the site:

## GET
**Syntax**: A GET command to `[endpoint]/api/eqn`, or simply entering the URL in a browser.

**Description**:
Either by going to `[endpoint]/api/eqn` in a browser, or making a GET request to `[endpoint]/api/eqn`, you can get a list of the current equations in the application's list.

## POST
**Syntax**: A POST command to `[endpoint]/api/eqn` with a JSON input in the format of:

    {
        "a": [number value],
        "op": ["a", "s", "d", or "m"]†
        "b": [number value]
    }
For the first operand, the operator, and the second operand, respectively.

**†** `"a"` for Addition, `"s"` for Subtraction, `"d"` for Division, and `"m"` for Multiplication. The dagger is not part of the code!

**Description**:
This command will add another equation into the API's list of equations. The result is calculated on generating the equation. 

## PUT
**Syntax**: A PUT command to `[endpoint]/api/eqn` with a JSON input in the same format as the POST command.

**Description**:
This command will, instead of adding a new equation to the list of recent equations, replace the most recently added equation. If the list is currently empty, the PUT command will add the equation to the otherwise empty list of recent equations.

## DELETE
**Syntax**: A DELETE command to `[endpoint]/api/eqn` with no other input.

**Description**:
This command will empty the list of recent equations and return a string confirming the action.

# Additional Notes

If you are unsure how to send GET/POST/PUT/DELETE (Or, generally, REST) commands to an endpoint, I suggest either [Postman](https://www.postman.com/), [Insomnia](https://insomnia.rest/), or, if you don't want to download anything, [APIReqeuest.io](https://www.apirequest.io/).
