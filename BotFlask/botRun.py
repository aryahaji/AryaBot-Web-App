headers = {
         "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    profile = Profile.query.get(1)
    form = CheckoutForm()
    
    s = requests.Session()
    s.headers.update(headers)

    #returns a list of the sizes that are in stock
    product_url = profile.url
    page = s.get(product_url).text
    soup = BeautifulSoup(page, "html.parser")
    sizeElem = soup.find("div", {"class":"box_wrapper"})
    sizes = sizeElem.findAll("a")
    availSizes = []
    for size in sizes:
        #sizes that are out of stock have class name box piunavailable
        if "box piunavailable" not in size["class"]:
            sizeID = size["id"]
            #sizeID example "itemcode_11111111". The first part is useless so we are adding only the number to the array that will contain sizes that are in stock
            availSizes.append(sizeID.split("_")[1])
    
    #adds a random size from the list of available sizes to cart and checks out
    randSize = random.choice(availSizes)

    #GET request for adding to cart puts the sizeID after add/ in the link so it will fill that with random size and add to cart
    atcUrl = "http://www.jimmyjazz.com/cart-request/cart/add/%s/1"%(randSize)

    page = s.get(atcUrl).text
    if '"success":1' in page:
        flash("Added To Cart!", 'success')
    checkoutUrl = "https://www.jimmyjazz.com/cart/checkout"
    page = s.get(checkoutUrl).text
    soup = BeautifulSoup(page, "html.parser")
    formInput = soup.find("input", {"name":"form_build_id"})
    formBuildId = formInput["value"]
    formData = {
        "billing_email": request.form['email'],
        "billing_email_confirm": request.form['email'],
        "billing_phone": request.form['phone'],
        "email_opt_in": "1",
        "shipping_first_name": request.form['firstName'],
        "shipping_last_name": request.form['lastName'],
        "shipping_country_html": request.form['country'],
        "shipping_address1": request.form['address'],
        "shipping_address2": request.form['address1'],
        "shipping_city": request.form['city'],
        "shipping_state": request.form['state'],
        "shipping_zip": request.form['zipCode'],
        "shipping_method": 1,
        "billing_same_as_shipping": 1,
        "billing_first_name": "",
        "billing_last_name": "",
        "billing_country": request.form['country'],
        "billing_address1": "",
        "billing_address2": "",
        "billing_city": "",
        "billing_state": "",
        "billing_zip": "",
        "payment_type": "credit_card",
        "cc_type": "",
        "cc_number": request.form['cc'],
        "cc_exp_month": request.form['expMonth'],
        "cc_exp_year": request.form['expYear'],
        "cc_cvv": request.form['cvv'],
        "gc_num": "",
        "form_build_id": formBuildId,
        "form_id": "cart_checkout_form"
    }
    pagePost = s.post(checkoutUrl, data=formData).text
    soup = BeautifulSoup(pagePost, "html.parser")
    elem = soup.find("input", {"name":"form_build_id"})
    formBuildId = elem["value"]
    confirmOrder = "https://www.jimmyjazz.com/cart/confirm"
    data = {
        "form_build_id": formBuildId,
        "form_id": "cart_confirm_form"
    }
    pagePostConfirm = s.post(confirmOrder, data=data)

    #tweepy. Private keys for API are in .env file
    consumer_key=""
    consumer_secret=""
    access_token=""
    access_token_secret=""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #tweets success tweet as well as product url if checkout was a success
    if '"success":1' in pagePostConfirm:
        flash("Successfully Checkout Out!", 'success')
        api.update_status("Successfully checkout out! " + product_url)
    else:
        flash("Checkout Unsuccessful", 'danger')
    return render_template('index.html', form=form)
