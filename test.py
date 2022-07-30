import requests

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

response = requests.get(
    "https://hackthebox.store/cart/30942215241867:1", headers=headers
)

print(response.url)
# req1

# req2
import requests

headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    "Accept": "application/json",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    "Origin": "https://checkout.shopifycs.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://checkout.shopifycs.com/",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

json_data = {
    "credit_card": {
        "number": "4427 5670 3287 3619",
        "name": "Jenna M Ortega",
        "month": 8,
        "year": 2025,
        "verification_value": "063",
        "start_month": None,
        "start_year": None,
        "issue_number": "",
    },
    "payment_session_scope": "hackthebox.store",
}

response = requests.post(
    "https://deposit.us.shopifycs.com/sessions", headers=headers, json=json_data
)

# req3
import requests

cookies = {
    "keep_alive": "81f19640-d53b-4629-b0f8-135289589a50",
    "secure_customer_sig": "",
    "localization": "GB",
    "cart_currency": "GBP",
    "_orig_referrer": "https%3A%2F%2Fwww.hackthebox.com%2F",
    "_landing_page": "%2Fproducts%2Fswag-card",
    "_y": "479389b7-e595-4647-acb9-2fb0c9bceb60",
    "_shopify_y": "479389b7-e595-4647-acb9-2fb0c9bceb60",
    "_fbp": "fb.1.1659093699007.752706045",
    "_g1645186687": "R0JQ",
    "cart": "1ebc539da44b9c4c591bd548b1f7075d",
    "cart_sig": "f7accc4768ac14177fc6cc56a2dc9d49",
    "ba_cart_token": "1ebc539da44b9c4c591bd548b1f7075d",
    "cart_ts": "1659093861",
    "checkout_session_token__c__1ebc539da44b9c4c591bd548b1f7075d": "%7B%22token%22%3A%22dThSWFlxRTRFbjRVOGlqb0YrZVYrK0JteHBIa05SQ3h3WmxKNGRhaThGVzlDNWlwNFBXNHJrYzB3STJROEFETmx1a0ZlWWI1VnFyd1gxV3JzMlA1QnF3akRIUWh6a0M1TDdha2xKVU1JMzE1S1ZJbXR6VXB3S3NuUFRGQ1lKSVRkdDljeWJyZVpTY1U1WlZGbVZaQW1xcmhJZFhKWnhudCtYck1kNlA2Zk9Bb0pzUWxXUHVhSEFhRnpwdlpuWkNPT1NHbHM4LzVLd3ZpVDc3TmZvRFh4MllIaVZyVVJKODU3NGpMWlZEMlFESmdhMFFzMUI5YzlqdUlsRk9hcjR0WGkvQ0pPcVJOWWNoTUthd3AtLXZBbjJ0Mi96bmNqWExGUU8tLTR4SE8rUHpwaGNGU3BYdEwzK3o3cXc9PQ%22%2C%22locale%22%3A%22en-GB%22%7D",
    "checkout_session_lookup": "%7B%22version%22%3A1%2C%22keys%22%3A%5B%7B%22source_id%22%3A%221ebc539da44b9c4c591bd548b1f7075d%22%2C%22checkout_session_identifier%22%3A%22900008daaf459d59854a8045d1967499%22%2C%22source_type_abbrev%22%3A%22c%22%2C%22updated_at%22%3A%222022-07-29T11%3A24%3A21.485Z%22%7D%5D%7D",
    "checkout_one_experiment": "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJZ0lIQVhzaVpYaHdaWEpwYldWdWRGOXVZVzFsSWpvaVl6RmZZV0pmZEdWemRGOHhOQ0lzSW1sdVgzUmxjM1JmWjNKdmRYQWlPblJ5ZFdVc0ltTmhjblJmZEc5clpXNGlPaUl4WldKak5UTTVaR0UwTkdJNVl6UmpOVGt4WW1RMU5EaGlNV1kzTURjMVpDSXNJbk4xWW1wbFkzUmZhV1FpT2lJNU1EQXdNRGhrWVdGbU5EVTVaRFU1T0RVMFlUZ3dORFZrTVRrMk56UTVPU0lzSW5OMFlYSjBhVzVuWDJ4dlkyRnNaU0k2SW1WdUxVZENJaXdpZG1WeWMybHZiaUk2SW1NeExtRmlYMlY0Y0dWeWFXMWxiblJmWTI5dmEybGxYM1psY25OcGIyNHVNUzQxSWl3aVpYaHdhWEpsY3lJNklqSXdNakl0TURndE1ERlVNVEU2TWpRNk1qRXVORGc0V2lKOUJqb0dSVlE9IiwiZXhwIjoiMjAyMi0wOC0wMVQxMToyNDoyMS40ODhaIiwicHVyIjoiY29va2llLmNoZWNrb3V0X29uZV9leHBlcmltZW50In19--831581103fa7db9ae8b6ab3f0ed7978beb44c5da",
    "cart_ver": "gcp-us-central1%3A3",
    "hide_shopify_pay_for_checkout": "false",
    "queue_token": "AlSioOTsPg3oBqiIVZYzfELyggZIxnXXVwMOVLREPcFcSDB5LWM0AVXcYoob2aAw8O9C4wx0nvDfdxfjlb4b7Oeq8QzK1XwvGy-mZp2j7H9oYGqKbR0rp0TFz3x18e-ygo-DFTRJXyPRam-VIMQD2rkmzD02tkLF1cZWhLipL8kjcPNYDBI=",
    "_shopify_sa_t": "2022-07-29T12%3A26%3A30.897Z",
    "_shopify_sa_p": "",
    "unique_interaction_id": "d209b0635ed81-128766426add8d-11bde29c34201d-31d36004f668d",
}

headers = {
    "authority": "hackthebox.store",
    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    "accept-language": "en-GB",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    # Already added when you pass json=
    # 'content-type': 'application/json',
    "accept": "application/json",
    "x-checkout-web-deploy-stage": "canary",
    "x-checkout-web-source-id": "1ebc539da44b9c4c591bd548b1f7075d",
    "x-checkout-web-build-id": "bb8a828973319943562603891d2368cf63971ab0",
    "origin": "https://hackthebox.store",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://hackthebox.store/",
    # Requests sorts cookies= alphabetically
    # 'cookie': 'keep_alive=81f19640-d53b-4629-b0f8-135289589a50; secure_customer_sig=; localization=GB; cart_currency=GBP; _orig_referrer=https%3A%2F%2Fwww.hackthebox.com%2F; _landing_page=%2Fproducts%2Fswag-card; _y=479389b7-e595-4647-acb9-2fb0c9bceb60; _shopify_y=479389b7-e595-4647-acb9-2fb0c9bceb60; _fbp=fb.1.1659093699007.752706045; _g1645186687=R0JQ; cart=1ebc539da44b9c4c591bd548b1f7075d; cart_sig=f7accc4768ac14177fc6cc56a2dc9d49; ba_cart_token=1ebc539da44b9c4c591bd548b1f7075d; cart_ts=1659093861; checkout_session_token__c__1ebc539da44b9c4c591bd548b1f7075d=%7B%22token%22%3A%22dThSWFlxRTRFbjRVOGlqb0YrZVYrK0JteHBIa05SQ3h3WmxKNGRhaThGVzlDNWlwNFBXNHJrYzB3STJROEFETmx1a0ZlWWI1VnFyd1gxV3JzMlA1QnF3akRIUWh6a0M1TDdha2xKVU1JMzE1S1ZJbXR6VXB3S3NuUFRGQ1lKSVRkdDljeWJyZVpTY1U1WlZGbVZaQW1xcmhJZFhKWnhudCtYck1kNlA2Zk9Bb0pzUWxXUHVhSEFhRnpwdlpuWkNPT1NHbHM4LzVLd3ZpVDc3TmZvRFh4MllIaVZyVVJKODU3NGpMWlZEMlFESmdhMFFzMUI5YzlqdUlsRk9hcjR0WGkvQ0pPcVJOWWNoTUthd3AtLXZBbjJ0Mi96bmNqWExGUU8tLTR4SE8rUHpwaGNGU3BYdEwzK3o3cXc9PQ%22%2C%22locale%22%3A%22en-GB%22%7D; checkout_session_lookup=%7B%22version%22%3A1%2C%22keys%22%3A%5B%7B%22source_id%22%3A%221ebc539da44b9c4c591bd548b1f7075d%22%2C%22checkout_session_identifier%22%3A%22900008daaf459d59854a8045d1967499%22%2C%22source_type_abbrev%22%3A%22c%22%2C%22updated_at%22%3A%222022-07-29T11%3A24%3A21.485Z%22%7D%5D%7D; checkout_one_experiment=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJZ0lIQVhzaVpYaHdaWEpwYldWdWRGOXVZVzFsSWpvaVl6RmZZV0pmZEdWemRGOHhOQ0lzSW1sdVgzUmxjM1JmWjNKdmRYQWlPblJ5ZFdVc0ltTmhjblJmZEc5clpXNGlPaUl4WldKak5UTTVaR0UwTkdJNVl6UmpOVGt4WW1RMU5EaGlNV1kzTURjMVpDSXNJbk4xWW1wbFkzUmZhV1FpT2lJNU1EQXdNRGhrWVdGbU5EVTVaRFU1T0RVMFlUZ3dORFZrTVRrMk56UTVPU0lzSW5OMFlYSjBhVzVuWDJ4dlkyRnNaU0k2SW1WdUxVZENJaXdpZG1WeWMybHZiaUk2SW1NeExtRmlYMlY0Y0dWeWFXMWxiblJmWTI5dmEybGxYM1psY25OcGIyNHVNUzQxSWl3aVpYaHdhWEpsY3lJNklqSXdNakl0TURndE1ERlVNVEU2TWpRNk1qRXVORGc0V2lKOUJqb0dSVlE9IiwiZXhwIjoiMjAyMi0wOC0wMVQxMToyNDoyMS40ODhaIiwicHVyIjoiY29va2llLmNoZWNrb3V0X29uZV9leHBlcmltZW50In19--831581103fa7db9ae8b6ab3f0ed7978beb44c5da; cart_ver=gcp-us-central1%3A3; hide_shopify_pay_for_checkout=false; queue_token=AlSioOTsPg3oBqiIVZYzfELyggZIxnXXVwMOVLREPcFcSDB5LWM0AVXcYoob2aAw8O9C4wx0nvDfdxfjlb4b7Oeq8QzK1XwvGy-mZp2j7H9oYGqKbR0rp0TFz3x18e-ygo-DFTRJXyPRam-VIMQD2rkmzD02tkLF1cZWhLipL8kjcPNYDBI=; _shopify_sa_t=2022-07-29T12%3A26%3A30.897Z; _shopify_sa_p=; unique_interaction_id=d209b0635ed81-128766426add8d-11bde29c34201d-31d36004f668d',
}

json_data = {
    "query": "mutation SubmitForCompletion($input:NegotiationInput!,$attemptToken:String!,$metafields:[MetafieldInput!],$postPurchaseInquiryResult:PostPurchaseInquiryResultCode){submitForCompletion(input:$input attemptToken:$attemptToken metafields:$metafields postPurchaseInquiryResult:$postPurchaseInquiryResult){...on SubmitSuccess{receipt{...ReceiptDetails __typename}__typename}...on SubmitAlreadyAccepted{receipt{...ReceiptDetails __typename}__typename}...on SubmitFailed{reason __typename}...on SubmitRejected{buyerProposal{...BuyerProposalDetails __typename}sellerProposal{...ProposalDetails __typename}violations{...on NegotiationError{code localizedMessage nonLocalizedMessage localizedMessageHtml...on RemoveTermViolation{message{code localizedDescription __typename}target __typename}...on AcceptNewTermViolation{message{code localizedDescription __typename}target __typename}...on ConfirmChangeViolation{message{code localizedDescription __typename}from to __typename}...on UnprocessableTermViolation{message{code localizedDescription __typename}target __typename}...on UnresolvableTermViolation{message{code localizedDescription __typename}target __typename}...on InputValidationError{field __typename}__typename}__typename}__typename}...on Throttled{pollAfter pollUrl queueToken buyerProposal{...BuyerProposalDetails __typename}__typename}...on CheckpointDenied{redirectUrl __typename}__typename}}fragment ReceiptDetails on Receipt{...on ProcessedReceipt{id token classicThankYouPageUrl orderIdentity{buyerIdentifier __typename}purchaseOrder{...ReceiptPurchaseOrder __typename}orderCreationStatus{__typename}postPurchasePageRequested postPurchaseVaultedPaymentMethodStatus __typename}...on ProcessingReceipt{id pollDelay __typename}...on ActionRequiredReceipt{id action{...on CompletePaymentChallenge{offsiteRedirect url __typename}__typename}__typename}...on FailedReceipt{id processingError{...on InventoryClaimFailure{__typename}...on InventoryReservationFailure{__typename}...on OrderCreationFailure{paymentsHaveBeenReverted __typename}...on OrderCreationSchedulingFailure{__typename}...on PaymentFailed{code messageUntranslated __typename}...on DiscountUsageLimitExceededFailure{__typename}...on CustomerPersistenceFailure{__typename}__typename}__typename}__typename}fragment ReceiptPurchaseOrder on PurchaseOrder{__typename delivery{...on PurchaseOrderDeliveryTerms{deliveryLines{__typename deliveryStrategy{handle title description methodType pickupLocation{...on PickupInStoreLocation{name address{address1 address2 city countryCode zoneCode postalCode phone coordinates{latitude longitude __typename}__typename}instructions __typename}__typename}__typename}lineAmount{amount currencyCode __typename}destinationAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}__typename}groupType}__typename}__typename}payment{...on PurchaseOrderPaymentTerms{paymentLines{amount{amount currencyCode __typename}paymentMethod{...on DirectPaymentMethod{sessionId paymentMethodIdentifier billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on PurchaseOrderGiftCardPaymentMethod{code __typename}...on WalletPaymentMethod{name walletContent{...on ShopPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}sessionToken __typename}...on PaypalWalletContent{paypalBillingAddress:billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}email payerId token __typename}...on ApplePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}data signature version __typename}...on GooglePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}signature signedMessage protocolVersion __typename}...on FacebookPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}containerData containerId mode __typename}...on ShopifyInstallmentsWalletContent{autoPayEnabled billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}disclosureDetails{evidence id type __typename}installmentsToken sessionToken __typename}__typename}__typename}...on LocalPaymentMethod{paymentMethodIdentifier name billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on PaymentOnDeliveryMethod{additionalDetails paymentInstructions paymentMethodIdentifier __typename}...on OffsitePaymentMethod{paymentMethodIdentifier name billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on DeferredPaymentMethod{paymentTermsTemplate{id dueDate dueInDays translatedName __typename}__typename}__typename}__typename}__typename}__typename}buyerIdentity{...on PurchaseOrderBuyerIdentityTerms{contactMethod{...on PurchaseOrderEmailContactMethod{email __typename}...on PurchaseOrderSMSContactMethod{phoneNumber __typename}__typename}marketingConsent{...on PurchaseOrderEmailContactMethod{email __typename}...on PurchaseOrderSMSContactMethod{phoneNumber __typename}__typename}__typename}__typename}}fragment BuyerProposalDetails on Proposal{merchandiseDiscount{...ProposalDiscountFragment __typename}deliveryDiscount{...ProposalDiscountFragment __typename}delivery{...ProposalDeliveryFragment __typename}merchandise{...on FilledMerchandiseTerms{taxesIncluded merchandiseLines{merchandise{...SourceProvidedMerchandise...ProductVariantMerchandiseDetails...ContextualizedProductVariantMerchandiseDetails...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}quantity{...on ProposalMerchandiseQuantityByItem{items{...on IntValueConstraint{value __typename}__typename}__typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}recurringTotal{title interval intervalCount recurringPrice{amount currencyCode __typename}fixedPrice{amount currencyCode __typename}fixedPriceCount __typename}lineComponents{...LineComponentDetails __typename}__typename}__typename}__typename}runningTotal{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}total{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotalBeforeTaxesAndShipping{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotalTaxes{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotal{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}deferredTotal{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}subtotalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}taxes{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}dueAt __typename}hasOnlyDeferredShipping subtotalBeforeTaxesAndShipping{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}fragment ProposalDiscountFragment on DiscountTermsV2{__typename...on FilledDiscountTerms{lines{...DiscountLineDetailsFragment __typename}__typename}...on PendingTerms{pollDelay taskId __typename}...on UnavailableTerms{__typename}}fragment DiscountLineDetailsFragment on DiscountLine{allocations{...on DiscountAllocatedAllocationSet{__typename allocations{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}target{index targetType __typename}__typename}}__typename}discount{...on CustomDiscount{title presentationLevel signature signatureUuid type value{...on PercentageValue{percentage __typename}...on FixedAmountValue{appliesOnEachItem fixedAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}...on CodeDiscount{title code presentationLevel __typename}...on DiscountCodeTrigger{code __typename}...on AutomaticDiscount{presentationLevel title __typename}__typename}lineAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}fragment ProposalDeliveryFragment on DeliveryTerms{__typename...on FilledDeliveryTerms{intermediateRates progressiveRatesEstimatedTimeUntilCompletion shippingRatesStatusToken deliveryLines{destinationAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on Geolocation{country{code __typename}zone{code __typename}coordinates{latitude longitude __typename}__typename}...on PartialStreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}__typename}targetMerchandise{...on FilledMerchandiseLineTargetCollection{lines{merchandise{...SourceProvidedMerchandise...on ProductVariantMerchandise{id digest variantId title requiresShipping properties{...MerchandiseProperties __typename}__typename}...on ContextualizedProductVariantMerchandise{id digest variantId title requiresShipping sellingPlan{id digest name prepaid deliveriesPerBillingCycle subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}properties{...MerchandiseProperties __typename}__typename}...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}groupType selectedDeliveryStrategy{...on CompleteDeliveryStrategy{handle __typename}...on DeliveryStrategyReference{handle __typename}__typename}availableDeliveryStrategies{...on CompleteDeliveryStrategy{title handle custom description acceptsInstructions phoneRequired methodType carrierName shopPromise deliveryStrategyBreakdown{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}discountRecurringCycleLimit excludeFromDeliveryOptionPrice targetMerchandise{...on FilledMerchandiseLineTargetCollection{lines{merchandise{...SourceProvidedMerchandise...on ProductVariantMerchandise{id digest variantId title requiresShipping properties{...MerchandiseProperties __typename}__typename}...on ContextualizedProductVariantMerchandise{id digest variantId title requiresShipping sellingPlan{id digest name prepaid deliveriesPerBillingCycle subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}properties{...MerchandiseProperties __typename}__typename}...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}__typename}minDeliveryDateTime maxDeliveryDateTime deliveryPromisePresentmentTitle{short long __typename}estimatedTimeInTransit{...on IntIntervalConstraint{lowerBound upperBound __typename}...on IntValueConstraint{value __typename}__typename}amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}amountAfterDiscounts{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}pickupLocation{...on PickupInStoreLocation{address{address1 address2 city countryCode phone postalCode zoneCode __typename}instructions name __typename}...on PickupPointLocation{address{address1 address2 address3 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}__typename}businessHours{day openingTime closingTime __typename}carrierCode carrierName handle kind name __typename}__typename}__typename}__typename}__typename}__typename}...on PendingTerms{pollDelay taskId __typename}...on UnavailableTerms{__typename}}fragment SourceProvidedMerchandise on Merchandise{...on SourceProvidedMerchandise{__typename product{id title productType vendor __typename}digest variantId optionalIdentifier title subtitle taxable giftCard requiresShipping price{amount currencyCode __typename}deferredAmount{amount currencyCode __typename}image{one:transformedSrc(maxWidth:64,maxHeight:64)two:transformedSrc(maxWidth:128,maxHeight:128)four:transformedSrc(maxWidth:256,maxHeight:256)__typename}options{name value __typename}properties{...MerchandiseProperties __typename}taxCode taxesIncluded weight{value unit __typename}sku}__typename}fragment MerchandiseProperties on MerchandiseProperty{name value{...on MerchandisePropertyValueString{string:value __typename}...on MerchandisePropertyValueInt{int:value __typename}...on MerchandisePropertyValueFloat{float:value __typename}...on MerchandisePropertyValueBoolean{boolean:value __typename}...on MerchandisePropertyValueJson{json:value __typename}__typename}visible __typename}fragment ProductVariantMerchandiseDetails on ProductVariantMerchandise{id digest variantId title subtitle product{id vendor productType __typename}image{one:transformedSrc(maxWidth:64,maxHeight:64)two:transformedSrc(maxWidth:128,maxHeight:128)four:transformedSrc(maxWidth:256,maxHeight:256)__typename}properties{...MerchandiseProperties __typename}requiresShipping options{name value __typename}sellingPlan{id __typename}giftCard __typename}fragment ContextualizedProductVariantMerchandiseDetails on ContextualizedProductVariantMerchandise{id digest variantId title subtitle price{amount currencyCode __typename}product{id vendor productType __typename}image{one:transformedSrc(maxWidth:64,maxHeight:64)two:transformedSrc(maxWidth:128,maxHeight:128)four:transformedSrc(maxWidth:256,maxHeight:256)__typename}properties{...MerchandiseProperties __typename}requiresShipping options{name value __typename}sellingPlan{name id digest deliveriesPerBillingCycle prepaid subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}giftCard deferredAmount{amount currencyCode __typename}__typename}fragment LineComponentDetails on LineComponent{quantity totalAmountBeforeReductions{amount currencyCode __typename}totalAmountAfterDiscounts{amount currencyCode __typename}totalAmountAfterLineDiscounts{amount currencyCode __typename}checkoutPriceAfterDiscounts{amount currencyCode __typename}checkoutPriceBeforeReductions{amount currencyCode __typename}unitPrice{price{amount currencyCode __typename}measurement{referenceUnit referenceValue __typename}__typename}allocations{...on LineComponentDiscountAllocation{discountLine{...DiscountLineDetailsFragment __typename}allocation{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}amount{amount currencyCode __typename}__typename}__typename}__typename}fragment ProposalDetails on Proposal{merchandiseDiscount{...ProposalDiscountFragment __typename}deliveryDiscount{...ProposalDiscountFragment __typename}delivery{...on FilledDeliveryTerms{intermediateRates progressiveRatesEstimatedTimeUntilCompletion shippingRatesStatusToken deliveryLines{destinationAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on Geolocation{country{code __typename}zone{code __typename}coordinates{latitude longitude __typename}__typename}...on PartialStreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}__typename}targetMerchandise{...on FilledMerchandiseLineTargetCollection{lines{merchandise{...SourceProvidedMerchandise...on ProductVariantMerchandise{id digest variantId title requiresShipping properties{...MerchandiseProperties __typename}__typename}...on ContextualizedProductVariantMerchandise{id digest variantId title requiresShipping sellingPlan{id digest name prepaid deliveriesPerBillingCycle subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}properties{...MerchandiseProperties __typename}__typename}...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}groupType selectedDeliveryStrategy{...on CompleteDeliveryStrategy{handle __typename}__typename}availableDeliveryStrategies{...on CompleteDeliveryStrategy{title handle custom description acceptsInstructions phoneRequired methodType carrierName shopPromise deliveryStrategyBreakdown{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}discountRecurringCycleLimit excludeFromDeliveryOptionPrice targetMerchandise{...on FilledMerchandiseLineTargetCollection{lines{merchandise{...SourceProvidedMerchandise...on ProductVariantMerchandise{id digest variantId title requiresShipping properties{...MerchandiseProperties __typename}__typename}...on ContextualizedProductVariantMerchandise{id digest variantId title requiresShipping sellingPlan{id digest name prepaid deliveriesPerBillingCycle subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}properties{...MerchandiseProperties __typename}__typename}...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}__typename}minDeliveryDateTime maxDeliveryDateTime deliveryPromisePresentmentTitle{short long __typename}estimatedTimeInTransit{...on IntIntervalConstraint{lowerBound upperBound __typename}...on IntValueConstraint{value __typename}__typename}amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}amountAfterDiscounts{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}pickupLocation{...on PickupInStoreLocation{address{address1 address2 city countryCode phone postalCode zoneCode __typename}instructions name __typename}...on PickupPointLocation{address{address1 address2 address3 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}__typename}businessHours{day openingTime closingTime __typename}carrierCode carrierName handle kind name __typename}__typename}__typename}__typename}__typename}__typename}...on PendingTerms{pollDelay taskId __typename}...on UnavailableTerms{__typename}__typename}payment{...on FilledPaymentTerms{availablePayments{paymentMethod{...on AnyDirectPaymentMethod{__typename availablePaymentProviders{paymentMethodIdentifier name brands __typename}}...on AnyOffsitePaymentMethod{__typename availableOffsiteProviders{__typename paymentMethodIdentifier name paymentBrands}}...on DirectPaymentMethod{__typename paymentMethodIdentifier}...on GiftCardPaymentMethod{__typename}...on AnyRedeemablePaymentMethod{__typename availableRedemptionSources}...on AnyWalletPaymentMethod{availableWalletPaymentConfigs{...on PaypalWalletConfig{__typename name merchantId venmoEnabled payflow paymentMethodIdentifier}...on ShopPayWalletConfig{__typename name storefrontUrl guestCheckoutUrl loginUrl}...on ShopifyInstallmentsWalletConfig{__typename name availableLoanTypes maxPrice{amount currencyCode __typename}minPrice{amount currencyCode __typename}supportedCountries supportedCurrencies giftCardsNotAllowed subscriptionItemsNotAllowed ineligibleTestModeCheckout paymentMethodIdentifier}...on FacebookPayWalletConfig{__typename name partnerId partnerMerchantId supportedContainers acquirerCountryCode mode paymentMethodIdentifier}...on ApplePayWalletConfig{__typename name supportedNetworks paymentMethodIdentifier}...on GooglePayWalletConfig{__typename name allowedAuthMethods allowedCardNetworks gateway gatewayMerchantId merchantId authJwt environment paymentMethodIdentifier}...on AmazonPayClassicWalletConfig{__typename name}__typename}__typename}...on LocalPaymentMethodConfig{__typename paymentMethodIdentifier name displayName additionalParameters{...on IdealBankSelectionParameterConfig{__typename label options{label value __typename}}__typename}}...on AnyPaymentOnDeliveryMethod{__typename additionalDetails paymentInstructions paymentMethodIdentifier}...on PaymentOnDeliveryMethod{__typename additionalDetails paymentInstructions paymentMethodIdentifier}...on CustomPaymentMethod{id name additionalDetails paymentInstructions __typename}...on ManualPaymentMethodConfig{id name additionalDetails paymentInstructions paymentMethodIdentifier __typename}...on CustomPaymentMethodConfig{id name additionalDetails paymentInstructions paymentMethodIdentifier __typename}...on DeferredPaymentMethod{paymentTermsTemplate{id translatedName dueDate __typename}__typename}...on NoopPaymentMethod{__typename}__typename}__typename}paymentLines{...PaymentLines __typename}billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on PendingTerms{pollDelay __typename}...on UnavailableTerms{__typename}__typename}merchandise{...on FilledMerchandiseTerms{taxesIncluded merchandiseLines{merchandise{...SourceProvidedMerchandise...ProductVariantMerchandiseDetails...ContextualizedProductVariantMerchandiseDetails...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}quantity{...on ProposalMerchandiseQuantityByItem{items{...on IntValueConstraint{value __typename}__typename}__typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}recurringTotal{title interval intervalCount recurringPrice{amount currencyCode __typename}fixedPrice{amount currencyCode __typename}fixedPriceCount __typename}lineComponents{...LineComponentDetails __typename}__typename}__typename}__typename}note{customAttributes{key value __typename}message __typename}scriptFingerprint{signature signatureUuid lineItemScriptChanges paymentScriptChanges shippingScriptChanges __typename}buyerIdentity{...on FilledBuyerIdentityTerms{buyerIdentity{...on GuestProfile{presentmentCurrency countryCode __typename}...on CustomerProfile{id presentmentCurrency fullName firstName lastName countryCode email imageUrl acceptsMarketing phone billingAddresses{address{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}__typename}shippingAddresses{address{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}__typename}__typename}...on BusinessCustomerProfile{checkoutExperienceConfiguration{availablePaymentOptions checkoutCompletionTarget __typename}id presentmentCurrency fullName firstName lastName acceptsMarketing companyName countryCode email phone selectedCompanyLocation{id name __typename}billingAddress{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}shippingAddress{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}__typename}__typename}contactInfoV2{...on EmailFormContents{email __typename}...on SMSFormContents{phoneNumber __typename}__typename}marketingConsent{...on SMSMarketingConsent{value __typename}...on EmailMarketingConsent{value __typename}__typename}__typename}__typename}recurringTotals{title interval intervalCount recurringPrice{amount currencyCode __typename}fixedPrice{amount currencyCode __typename}fixedPriceCount __typename}subtotalBeforeTaxesAndShipping{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}runningTotal{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}total{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotalBeforeTaxesAndShipping{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotalTaxes{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotal{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}deferredTotal{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}subtotalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}taxes{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}dueAt __typename}hasOnlyDeferredShipping subtotalBeforeReductions{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}duty{...on FilledDutyTerms{totalDutyAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}totalTaxAndDutyAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}...on PendingTerms{pollDelay __typename}...on UnavailableTerms{__typename}__typename}tax{...on FilledTaxTerms{totalTaxAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}totalTaxAndDutyAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}totalAmountIncludedInTarget{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}exemptions{taxExemptionReason targets{...on TargetAllLines{__typename}__typename}__typename}__typename}...on PendingTerms{pollDelay __typename}...on UnavailableTerms{__typename}__typename}tip{...on FilledTipTerms{tipLines{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}tipSuggestions{...on TipSuggestion{__typename percentage amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}}__typename}__typename}__typename}localizationExtension{...on LocalizationExtension{fields{...on LocalizationExtensionField{key title value __typename}__typename}__typename}__typename}landedCostDetails{incotermInformation{incoterm reason __typename}__typename}nonNegotiableTerms{signature contents{signature targetTerms targetLine{allLines index __typename}attributes __typename}__typename}optionalDuties{buyerRefusesDuties refuseDutiesPermitted __typename}__typename}fragment PaymentLines on PaymentLine{specialInstructions amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}dueAt paymentMethod{...on DirectPaymentMethod{sessionId paymentMethodIdentifier __typename}...on GiftCardPaymentMethod{code balance{amount currencyCode __typename}__typename}...on RedeemablePaymentMethod{redemptionSource redemptionContent{...on ShopCashRedemptionContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}__typename}redemptionId __typename}__typename}__typename}...on WalletPaymentMethod{name walletContent{...on ShopPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}sessionToken __typename}...on PaypalWalletContent{paypalBillingAddress:billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}email payerId token paymentMethodIdentifier __typename}...on ApplePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}data signature version lastDigits paymentMethodIdentifier __typename}...on GooglePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}signature signedMessage protocolVersion paymentMethodIdentifier __typename}...on FacebookPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}containerData containerId mode paymentMethodIdentifier __typename}...on ShopifyInstallmentsWalletContent{autoPayEnabled billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}disclosureDetails{evidence id type __typename}installmentsToken sessionToken paymentMethodIdentifier __typename}__typename}__typename}...on LocalPaymentMethod{paymentMethodIdentifier name additionalParameters{...on IdealPaymentMethodParameters{bank __typename}__typename}__typename}...on PaymentOnDeliveryMethod{additionalDetails paymentInstructions paymentMethodIdentifier __typename}...on OffsitePaymentMethod{paymentMethodIdentifier name __typename}...on CustomPaymentMethod{id name additionalDetails paymentInstructions paymentMethodIdentifier __typename}...on ManualPaymentMethod{id name paymentMethodIdentifier __typename}...on DeferredPaymentMethod{paymentTermsTemplate{id translatedName dueDate __typename}__typename}...on NoopPaymentMethod{__typename}__typename}__typename}",
    "variables": {
        "input": {
            "checkpointData": None,
            "sessionInput": {
                "sessionToken": "dThSWFlxRTRFbjRVOGlqb0YrZVYrK0JteHBIa05SQ3h3WmxKNGRhaThGVzlDNWlwNFBXNHJrYzB3STJROEFETmx1a0ZlWWI1VnFyd1gxV3JzMlA1QnF3akRIUWh6a0M1TDdha2xKVU1JMzE1S1ZJbXR6VXB3S3NuUFRGQ1lKSVRkdDljeWJyZVpTY1U1WlZGbVZaQW1xcmhJZFhKWnhudCtYck1kNlA2Zk9Bb0pzUWxXUHVhSEFhRnpwdlpuWkNPT1NHbHM4LzVLd3ZpVDc3TmZvRFh4MllIaVZyVVJKODU3NGpMWlZEMlFESmdhMFFzMUI5YzlqdUlsRk9hcjR0WGkvQ0pPcVJOWWNoTUthd3AtLXZBbjJ0Mi96bmNqWExGUU8tLTR4SE8rUHpwaGNGU3BYdEwzK3o3cXc9PQ",
            },
            "queueToken": "AlSioOTsPg3oBqiIVZYzfELyggZIxnXXVwMOVLREPcFcSDB5LWM0AVXcYoob2aAw8O9C4wx0nvDfdxfjlb4b7Oeq8QzK1XwvGy-mZp2j7H9oYGqKbR0rp0TFz3x18e-ygo-DFTRJXyPRam-VIMQD2rkmzD02tkLF1cZWhLipL8kjcPNYDBI=",
            "discounts": {
                "lines": [],
                "acceptUnexpectedDiscounts": True,
            },
            "delivery": {
                "deliveryLines": [
                    {
                        "selectedDeliveryStrategy": {
                            "deliveryStrategyMatchingConditions": {
                                "estimatedTimeInTransit": {
                                    "any": True,
                                },
                                "shipments": {
                                    "any": True,
                                },
                            },
                            "options": {},
                        },
                        "targetMerchandiseLines": {
                            "lines": [
                                {
                                    "atIndex": 0,
                                },
                            ],
                        },
                        "deliveryMethodTypes": [
                            "NONE",
                        ],
                        "expectedTotalPrice": {
                            "any": True,
                        },
                        "destinationChanged": True,
                    },
                ],
                "noDeliveryRequired": [],
                "useProgressiveRates": True,
                "interfaceFlow": "SHOPIFY",
            },
            "merchandise": {
                "merchandiseLines": [
                    {
                        "merchandise": {
                            "productVariantReference": {
                                "id": "gid://shopify/ProductVariantMerchandise/30942215241867",
                                "variantId": "gid://shopify/ProductVariant/30942215241867",
                                "properties": [],
                                "sellingPlanId": None,
                                "sellingPlanDigest": None,
                            },
                        },
                        "quantity": {
                            "items": {
                                "value": 1,
                            },
                        },
                        "expectedTotalPrice": {
                            "value": {
                                "amount": "10.00",
                                "currencyCode": "GBP",
                            },
                        },
                    },
                ],
            },
            "payment": {
                "totalAmount": {
                    "any": True,
                },
                "paymentLines": [
                    {
                        "paymentMethod": {
                            "directPaymentMethod": {
                                "paymentMethodIdentifier": "2ea57f551052bc9409a1d3f00dd14386",
                                "sessionId": "east-789878c9d0f4139eb6c351af1a7baa8e",
                                "billingAddress": {
                                    "streetAddress": {
                                        "address1": "491",
                                        "address2": "d",
                                        "city": "Florence",
                                        "countryCode": "US",
                                        "postalCode": "41042",
                                        "firstName": "Jenna ",
                                        "lastName": "Charichilil",
                                        "zoneCode": "KY",
                                        "phone": "099615 17833",
                                    },
                                },
                            },
                            "giftCardPaymentMethod": None,
                            "redeemablePaymentMethod": None,
                            "walletPaymentMethod": None,
                            "localPaymentMethod": None,
                            "paymentOnDeliveryMethod": None,
                            "paymentOnDeliveryMethod2": None,
                            "manualPaymentMethod": None,
                            "customPaymentMethod": None,
                            "offsitePaymentMethod": None,
                            "deferredPaymentMethod": None,
                        },
                        "amount": {
                            "value": {
                                "amount": "10",
                                "currencyCode": "GBP",
                            },
                        },
                        "dueAt": None,
                    },
                ],
                "billingAddress": {
                    "streetAddress": {
                        "address1": "491",
                        "address2": "d",
                        "city": "Florence",
                        "countryCode": "US",
                        "postalCode": "41042",
                        "firstName": "Jenna ",
                        "lastName": "Charichilil",
                        "zoneCode": "KY",
                        "phone": "099615 17833",
                    },
                },
            },
            "buyerIdentity": {
                "buyerIdentity": {},
                "contactInfoV2": {
                    "emailOrSms": {
                        "value": "roseloverx@proton.me",
                        "emailOrSmsChanged": False,
                    },
                },
                "marketingConsent": [],
            },
            "tip": {
                "tipLines": [],
            },
            "taxes": {
                "proposedAllocations": None,
                "proposedTotalAmount": {
                    "value": {
                        "amount": "0",
                        "currencyCode": "GBP",
                    },
                },
                "proposedTotalIncludedAmount": None,
                "proposedMixedStateTotalAmount": None,
                "proposedExemptions": [],
            },
            "note": {
                "message": None,
                "customAttributes": [],
            },
            "localizationExtension": {
                "fields": [],
            },
            "nonNegotiableTerms": None,
        },
        "attemptToken": "1ebc539da44b9c4c591bd548b1f7075d-0.08081608622881853",
        "metafields": [],
    },
    "operationName": "SubmitForCompletion",
}

response = requests.post(
    "https://hackthebox.store/checkouts/unstable/graphql",
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# req4

cookies = {
    "keep_alive": "81f19640-d53b-4629-b0f8-135289589a50",
    "secure_customer_sig": "",
    "localization": "GB",
    "cart_currency": "GBP",
    "_orig_referrer": "https%3A%2F%2Fwww.hackthebox.com%2F",
    "_landing_page": "%2Fproducts%2Fswag-card",
    "_y": "479389b7-e595-4647-acb9-2fb0c9bceb60",
    "_shopify_y": "479389b7-e595-4647-acb9-2fb0c9bceb60",
    "_fbp": "fb.1.1659093699007.752706045",
    "_g1645186687": "R0JQ",
    "cart": "1ebc539da44b9c4c591bd548b1f7075d",
    "cart_sig": "f7accc4768ac14177fc6cc56a2dc9d49",
    "ba_cart_token": "1ebc539da44b9c4c591bd548b1f7075d",
    "cart_ts": "1659093861",
    "checkout_session_token__c__1ebc539da44b9c4c591bd548b1f7075d": "%7B%22token%22%3A%22dThSWFlxRTRFbjRVOGlqb0YrZVYrK0JteHBIa05SQ3h3WmxKNGRhaThGVzlDNWlwNFBXNHJrYzB3STJROEFETmx1a0ZlWWI1VnFyd1gxV3JzMlA1QnF3akRIUWh6a0M1TDdha2xKVU1JMzE1S1ZJbXR6VXB3S3NuUFRGQ1lKSVRkdDljeWJyZVpTY1U1WlZGbVZaQW1xcmhJZFhKWnhudCtYck1kNlA2Zk9Bb0pzUWxXUHVhSEFhRnpwdlpuWkNPT1NHbHM4LzVLd3ZpVDc3TmZvRFh4MllIaVZyVVJKODU3NGpMWlZEMlFESmdhMFFzMUI5YzlqdUlsRk9hcjR0WGkvQ0pPcVJOWWNoTUthd3AtLXZBbjJ0Mi96bmNqWExGUU8tLTR4SE8rUHpwaGNGU3BYdEwzK3o3cXc9PQ%22%2C%22locale%22%3A%22en-GB%22%7D",
    "checkout_session_lookup": "%7B%22version%22%3A1%2C%22keys%22%3A%5B%7B%22source_id%22%3A%221ebc539da44b9c4c591bd548b1f7075d%22%2C%22checkout_session_identifier%22%3A%22900008daaf459d59854a8045d1967499%22%2C%22source_type_abbrev%22%3A%22c%22%2C%22updated_at%22%3A%222022-07-29T11%3A24%3A21.485Z%22%7D%5D%7D",
    "checkout_one_experiment": "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJZ0lIQVhzaVpYaHdaWEpwYldWdWRGOXVZVzFsSWpvaVl6RmZZV0pmZEdWemRGOHhOQ0lzSW1sdVgzUmxjM1JmWjNKdmRYQWlPblJ5ZFdVc0ltTmhjblJmZEc5clpXNGlPaUl4WldKak5UTTVaR0UwTkdJNVl6UmpOVGt4WW1RMU5EaGlNV1kzTURjMVpDSXNJbk4xWW1wbFkzUmZhV1FpT2lJNU1EQXdNRGhrWVdGbU5EVTVaRFU1T0RVMFlUZ3dORFZrTVRrMk56UTVPU0lzSW5OMFlYSjBhVzVuWDJ4dlkyRnNaU0k2SW1WdUxVZENJaXdpZG1WeWMybHZiaUk2SW1NeExtRmlYMlY0Y0dWeWFXMWxiblJmWTI5dmEybGxYM1psY25OcGIyNHVNUzQxSWl3aVpYaHdhWEpsY3lJNklqSXdNakl0TURndE1ERlVNVEU2TWpRNk1qRXVORGc0V2lKOUJqb0dSVlE9IiwiZXhwIjoiMjAyMi0wOC0wMVQxMToyNDoyMS40ODhaIiwicHVyIjoiY29va2llLmNoZWNrb3V0X29uZV9leHBlcmltZW50In19--831581103fa7db9ae8b6ab3f0ed7978beb44c5da",
    "cart_ver": "gcp-us-central1%3A3",
    "hide_shopify_pay_for_checkout": "false",
    "queue_token": "AlSioOTsPg3oBqiIVZYzfELyggZIxnXXVwMOVLREPcFcSDB5LWM0AVXcYoob2aAw8O9C4wx0nvDfdxfjlb4b7Oeq8QzK1XwvGy-mZp2j7H9oYGqKbR0rp0TFz3x18e-ygo-DFTRJXyPRam-VIMQD2rkmzD02tkLF1cZWhLipL8kjcPNYDBI=",
    "_shopify_sa_p": "",
    "_shopify_sa_t": "2022-07-29T12%3A27%3A56.567Z",
    "unique_interaction_id": "11fd8b7b3855d9-d129c51ef0923-aa0f32c9fd4e3-bda8598d1d27b",
}

headers = {
    "authority": "hackthebox.store",
    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    "accept-language": "en-GB",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    # Already added when you pass json=
    # 'content-type': 'application/json',
    "accept": "application/json",
    "x-checkout-web-deploy-stage": "canary",
    "x-checkout-web-source-id": "1ebc539da44b9c4c591bd548b1f7075d",
    "x-checkout-web-build-id": "bb8a828973319943562603891d2368cf63971ab0",
    "origin": "https://hackthebox.store",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://hackthebox.store/",
    # Requests sorts cookies= alphabetically
    # 'cookie': 'keep_alive=81f19640-d53b-4629-b0f8-135289589a50; secure_customer_sig=; localization=GB; cart_currency=GBP; _orig_referrer=https%3A%2F%2Fwww.hackthebox.com%2F; _landing_page=%2Fproducts%2Fswag-card; _y=479389b7-e595-4647-acb9-2fb0c9bceb60; _shopify_y=479389b7-e595-4647-acb9-2fb0c9bceb60; _fbp=fb.1.1659093699007.752706045; _g1645186687=R0JQ; cart=1ebc539da44b9c4c591bd548b1f7075d; cart_sig=f7accc4768ac14177fc6cc56a2dc9d49; ba_cart_token=1ebc539da44b9c4c591bd548b1f7075d; cart_ts=1659093861; checkout_session_token__c__1ebc539da44b9c4c591bd548b1f7075d=%7B%22token%22%3A%22dThSWFlxRTRFbjRVOGlqb0YrZVYrK0JteHBIa05SQ3h3WmxKNGRhaThGVzlDNWlwNFBXNHJrYzB3STJROEFETmx1a0ZlWWI1VnFyd1gxV3JzMlA1QnF3akRIUWh6a0M1TDdha2xKVU1JMzE1S1ZJbXR6VXB3S3NuUFRGQ1lKSVRkdDljeWJyZVpTY1U1WlZGbVZaQW1xcmhJZFhKWnhudCtYck1kNlA2Zk9Bb0pzUWxXUHVhSEFhRnpwdlpuWkNPT1NHbHM4LzVLd3ZpVDc3TmZvRFh4MllIaVZyVVJKODU3NGpMWlZEMlFESmdhMFFzMUI5YzlqdUlsRk9hcjR0WGkvQ0pPcVJOWWNoTUthd3AtLXZBbjJ0Mi96bmNqWExGUU8tLTR4SE8rUHpwaGNGU3BYdEwzK3o3cXc9PQ%22%2C%22locale%22%3A%22en-GB%22%7D; checkout_session_lookup=%7B%22version%22%3A1%2C%22keys%22%3A%5B%7B%22source_id%22%3A%221ebc539da44b9c4c591bd548b1f7075d%22%2C%22checkout_session_identifier%22%3A%22900008daaf459d59854a8045d1967499%22%2C%22source_type_abbrev%22%3A%22c%22%2C%22updated_at%22%3A%222022-07-29T11%3A24%3A21.485Z%22%7D%5D%7D; checkout_one_experiment=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJZ0lIQVhzaVpYaHdaWEpwYldWdWRGOXVZVzFsSWpvaVl6RmZZV0pmZEdWemRGOHhOQ0lzSW1sdVgzUmxjM1JmWjNKdmRYQWlPblJ5ZFdVc0ltTmhjblJmZEc5clpXNGlPaUl4WldKak5UTTVaR0UwTkdJNVl6UmpOVGt4WW1RMU5EaGlNV1kzTURjMVpDSXNJbk4xWW1wbFkzUmZhV1FpT2lJNU1EQXdNRGhrWVdGbU5EVTVaRFU1T0RVMFlUZ3dORFZrTVRrMk56UTVPU0lzSW5OMFlYSjBhVzVuWDJ4dlkyRnNaU0k2SW1WdUxVZENJaXdpZG1WeWMybHZiaUk2SW1NeExtRmlYMlY0Y0dWeWFXMWxiblJmWTI5dmEybGxYM1psY25OcGIyNHVNUzQxSWl3aVpYaHdhWEpsY3lJNklqSXdNakl0TURndE1ERlVNVEU2TWpRNk1qRXVORGc0V2lKOUJqb0dSVlE9IiwiZXhwIjoiMjAyMi0wOC0wMVQxMToyNDoyMS40ODhaIiwicHVyIjoiY29va2llLmNoZWNrb3V0X29uZV9leHBlcmltZW50In19--831581103fa7db9ae8b6ab3f0ed7978beb44c5da; cart_ver=gcp-us-central1%3A3; hide_shopify_pay_for_checkout=false; queue_token=AlSioOTsPg3oBqiIVZYzfELyggZIxnXXVwMOVLREPcFcSDB5LWM0AVXcYoob2aAw8O9C4wx0nvDfdxfjlb4b7Oeq8QzK1XwvGy-mZp2j7H9oYGqKbR0rp0TFz3x18e-ygo-DFTRJXyPRam-VIMQD2rkmzD02tkLF1cZWhLipL8kjcPNYDBI=; _shopify_sa_p=; _shopify_sa_t=2022-07-29T12%3A27%3A56.567Z; unique_interaction_id=11fd8b7b3855d9-d129c51ef0923-aa0f32c9fd4e3-bda8598d1d27b',
}

json_data = {
    "query": "query PollForReceipt($receiptId:ID!,$sessionToken:String!){receipt(receiptId:$receiptId,sessionInput:{sessionToken:$sessionToken}){...ReceiptDetails __typename}}fragment ReceiptDetails on Receipt{...on ProcessedReceipt{id token classicThankYouPageUrl orderIdentity{buyerIdentifier __typename}purchaseOrder{...ReceiptPurchaseOrder __typename}orderCreationStatus{__typename}postPurchasePageRequested postPurchaseVaultedPaymentMethodStatus __typename}...on ProcessingReceipt{id pollDelay __typename}...on ActionRequiredReceipt{id action{...on CompletePaymentChallenge{offsiteRedirect url __typename}__typename}__typename}...on FailedReceipt{id processingError{...on InventoryClaimFailure{__typename}...on InventoryReservationFailure{__typename}...on OrderCreationFailure{paymentsHaveBeenReverted __typename}...on OrderCreationSchedulingFailure{__typename}...on PaymentFailed{code messageUntranslated __typename}...on DiscountUsageLimitExceededFailure{__typename}...on CustomerPersistenceFailure{__typename}__typename}__typename}__typename}fragment ReceiptPurchaseOrder on PurchaseOrder{__typename delivery{...on PurchaseOrderDeliveryTerms{deliveryLines{__typename deliveryStrategy{handle title description methodType pickupLocation{...on PickupInStoreLocation{name address{address1 address2 city countryCode zoneCode postalCode phone coordinates{latitude longitude __typename}__typename}instructions __typename}__typename}__typename}lineAmount{amount currencyCode __typename}destinationAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}__typename}groupType}__typename}__typename}payment{...on PurchaseOrderPaymentTerms{paymentLines{amount{amount currencyCode __typename}paymentMethod{...on DirectPaymentMethod{sessionId paymentMethodIdentifier billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on PurchaseOrderGiftCardPaymentMethod{code __typename}...on WalletPaymentMethod{name walletContent{...on ShopPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}sessionToken __typename}...on PaypalWalletContent{paypalBillingAddress:billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}email payerId token __typename}...on ApplePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}data signature version __typename}...on GooglePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}signature signedMessage protocolVersion __typename}...on FacebookPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}containerData containerId mode __typename}...on ShopifyInstallmentsWalletContent{autoPayEnabled billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}disclosureDetails{evidence id type __typename}installmentsToken sessionToken __typename}__typename}__typename}...on LocalPaymentMethod{paymentMethodIdentifier name billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on PaymentOnDeliveryMethod{additionalDetails paymentInstructions paymentMethodIdentifier __typename}...on OffsitePaymentMethod{paymentMethodIdentifier name billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on DeferredPaymentMethod{paymentTermsTemplate{id dueDate dueInDays translatedName __typename}__typename}__typename}__typename}__typename}__typename}buyerIdentity{...on PurchaseOrderBuyerIdentityTerms{contactMethod{...on PurchaseOrderEmailContactMethod{email __typename}...on PurchaseOrderSMSContactMethod{phoneNumber __typename}__typename}marketingConsent{...on PurchaseOrderEmailContactMethod{email __typename}...on PurchaseOrderSMSContactMethod{phoneNumber __typename}__typename}__typename}__typename}}",
    "variables": {
        "receiptId": "gid://shopify/ProcessedReceipt/1052582969502",
        "sessionToken": "dThSWFlxRTRFbjRVOGlqb0YrZVYrK0JteHBIa05SQ3h3WmxKNGRhaThGVzlDNWlwNFBXNHJrYzB3STJROEFETmx1a0ZlWWI1VnFyd1gxV3JzMlA1QnF3akRIUWh6a0M1TDdha2xKVU1JMzE1S1ZJbXR6VXB3S3NuUFRGQ1lKSVRkdDljeWJyZVpTY1U1WlZGbVZaQW1xcmhJZFhKWnhudCtYck1kNlA2Zk9Bb0pzUWxXUHVhSEFhRnpwdlpuWkNPT1NHbHM4LzVLd3ZpVDc3TmZvRFh4MllIaVZyVVJKODU3NGpMWlZEMlFESmdhMFFzMUI5YzlqdUlsRk9hcjR0WGkvQ0pPcVJOWWNoTUthd3AtLXZBbjJ0Mi96bmNqWExGUU8tLTR4SE8rUHpwaGNGU3BYdEwzK3o3cXc9PQ",
    },
    "operationName": "PollForReceipt",
}

response = requests.post(
    "https://hackthebox.store/checkouts/unstable/graphql",
    cookies=cookies,
    headers=headers,
    json=json_data,
)
