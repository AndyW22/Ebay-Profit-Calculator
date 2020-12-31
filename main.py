import PySimpleGUIQt as sg
import lib

sg.theme("Dark")

# Purchase frame layout
purchased_frame = [
    [sg.Text("Shop")],
    [sg.Combo(["Ebay", "Bank transfer", "Shpock"], default_value="Ebay", readonly=True, pad=((2, 2), (5, 5)), size=(20, 1), key="shop1")],
    [sg.Text("Price")],
    [sg.Text("£", font=("Helvetica", 15)), sg.InputText(default_text="1.00", size=(7, 1), pad=((2, 2), (5, 5)), key="price1", enable_events=True)],
    [sg.Text("Delivery cost")],
    [sg.Text("£", font=("Helvetica", 15)), sg.InputText(default_text="1.00", size=(7, 1), pad=((2, 2), (5, 5)), key="postage1", enable_events=True)],
]

# Sold frame layout
sold_frame = [
    [sg.Text("Shop")],
    [sg.Combo(["Ebay", "Bank transfer"], default_value="Ebay", readonly=True, pad=((2, 2), (5, 5)), size=(20, 1), key="shop2")],
    [sg.Text("Sale Price")],
    [sg.Text("£", font=("Helvetica", 15)), sg.InputText(default_text="1.00", size=(7, 1), pad=((2, 2), (5, 5)), key="price2", enable_events=True)],
    [sg.Text("Shipping Surcharge")],
    [sg.Text("£", font=("Helvetica", 15)), sg.InputText(default_text="0.00", size=(7, 1), pad=((2, 2), (5, 5)), key="shippingcharge", enable_events=True)],
    [sg.Text("Delivery cost")],
    [sg.Text("£", font=("Helvetica", 15)), sg.InputText(default_text="1.00", size=(7, 1), pad=((2, 2), (5, 5)), key="postage2", enable_events=True)],
    [sg.Text("Fee Percentage (for Ebay shops only, 10% for private sellers)")],
    [sg.Text("%", font=("Helvetica", 15)), sg.InputText(default_text="10", size=(7, 1), pad=((2, 2), (5, 5)), key="fee", enable_events=True)],
]

# Controls and output frame layout
controls_frame = [
    [sg.Button("Calculate profit", 	border_width=1, size=(15, 1), font=("Segoe", 13), auto_size_button=True, key="-CALC-"), sg.MultilineOutput("", key="-STATE-", font=("Helvetica", 10), size=(20, 3)), sg.VerticalSeparator(pad=((2, 2), (5, 5))), sg.Text("Profit: £ ", key="-OUTPUT-", size=(22, 2))]
]


# Window layout
layout = [  
    [sg.Frame("Purchased", purchased_frame, pad=((100, 100), (100, 100))), sg.Frame("Sold", sold_frame, pad=((100, 100),(100,100)))],
    [sg.Frame("Controls", controls_frame, pad=((100, 100), (30, 100)))]
]

# Create the Window
window = sg.Window('Profit Calculator App', layout, icon="icon.png")

# Event Loop to process events

input_cache = ["1.00", "1.00", "1.00", "1.00", "10"]

while True:             
    event, values = window.read()
    # Handle exiting
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    # Float input handler, checks if new input is castable into a float, if not replace with cache
    if event == "price1":
        try:
            if len(values['price1']) != 0:
                float(values['price1'])
        except ValueError:
            window['price1'].update(value=input_cache[0])

    if event == "price2":
        try:
            if len(values['price2']) != 0:
                float(values['price2'])
        except ValueError:
            window['price2'].update(value=input_cache[0])

    if event == "postage1":
        try:
            if len(values['postage1']) != 0:
                float(values['postage1'])
        except ValueError:
            window['postage1'].update(value=input_cache[0])

    if event == "postage2":
        try:
            if len(values['postage2']) != 0:
                float(values['postage2'])
        except ValueError:
            window['postage2'].update(value=input_cache[0])

    if event == "fee":
        try:
            if len(values['fee']) != 0:
                float(values['fee'])
        except ValueError:
            window['fee'].update(value=input_cache[0])

    if event == "shippingcharge":
        try:
            if len(values['shippingcharge']) != 0:
                float(values['shippingcharge'])
        except ValueError:
            window['shippingcharge'].update(value=input_cache[0])

    input_cache = [values['price1'], values['price2'], values['postage1'], values['postage2'], values['fee'], values['shippingcharge']]
    # Calculate profit button event
    if event == "-CALC-":
        window['-STATE-'].update(value="")

        # Check and handle invalid entries
        if float(values['price1']) < 0 or float(values['price2']) < 0 or float(values['postage1']) < 0 or float(
                values['postage2']) < 0:
            window['-STATE-'].update(value="Price/Delivery cost cannot be negative.", text_color="orange")
        elif float(values['fee']) < 0:
            window['-STATE-'].update(value="Fee percentage cannot be negative", text_color="red")

        else:
            # Run calculations
            if values['shop1'] in ("Ebay", "Bank transfer"):
                profit = lib.ebay(float(values['price1']), float(values['postage1']), float(values['price2']), float(values['postage2']), values["shop2"], float(values["fee"]), float(values["shippingcharge"]))
            else:
                profit = lib.shpock(float(values['price1']), float(values['postage1']), float(values['price2']), float(values['postage2']), values["shop2"], float(values["fee"]))
            if values['shop2'] in ("Ebay"):
                paypalfee = lib.paypalfee(float(values['price2']), float(values['shippingcharge']))
                ebayfee = lib.ebayfee(float(values['price2']), float(values['shippingcharge']), float(values['fee']))
            # Handle results
            if values['shop2'] in "Ebay" and (profit > 0):
                if profit - 0.36 > 0:
                    window['-STATE-'].update(value="You will make a profit.", text_color="green")
                    window['-OUTPUT-'].update(value=(f"Total Profit: £{round(profit, 2):.2f}" + "\n" + f"Total Profit incl insertion fee: £{round(profit - 0.36, 2):.2f}" + "\n" + f"Paypal Fee: £{round(paypalfee, 2):.2f}" + "\n" + f"Ebay Fee: £{round(ebayfee, 2):.2f}"))
                else:
                    window['-STATE-'].update(value="You will make a loss if you are a private seller.", text_color="orange")
                    window['-OUTPUT-'].update(value=(f"Total Profit (Business Seller): £{round(profit, 2):.2f}" + "\n" + f"Paypal Fee: £{round(paypalfee, 2):.2f}" + "\n" + f"Total Losses incl insertion fee: £{round(abs(profit - 0.36), 2):.2f}" + "\n" + f"Ebay Fee: £{round(ebayfee, 2):.2f}"))
            elif values['shop2'] in "Ebay" and (profit < 0):
                window['-STATE-'].update(value="You will make a loss.", text_color="red")
                window['-OUTPUT-'].update(value=(f"Total Losses: £{round(abs(profit), 2):.2f}" + "\n" + f"Total Losses incl insertion fee: £{round(abs(profit - 0.36), 2):.2f}" + "\n" + f"Paypal Fee: £{round(abs(paypalfee), 2):.2f}" + "\n" + f"Ebay Fee: £{round(ebayfee, 2):.2f}"))
            elif profit < 0:
                window['-STATE-'].update(value="You will lose money.", text_color="red")
                window['-OUTPUT-'].update(value="Total Losses £{:.2f} ".format(round(abs(profit), 2)))
            elif profit == 0:
                window['-STATE-'].update(value="You will break even.", text_color="yellow")
                window['-OUTPUT-'].update(value="Profit: £0.00 ")
            else:
                window['-STATE-'].update(value="You will make a profit.", text_color="green")
                window['-OUTPUT-'].update(value=f"Total Profit: £{round(profit, 2):.2f}")



window.close()
