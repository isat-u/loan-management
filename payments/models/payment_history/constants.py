PAYMENT_SOURCES = (
    ('cash', 'Cash'),
    ('gcash', 'GCash'),
    ('paymaya', 'PayMaya'),
    ('paymongo', 'PayMongo'),
    ('paypal', 'PayPal'),
)

CURRENCY_CHOICES = (
    ('PHP', 'Philippine Peso'),
)

INVOICE_PAD = '0000000000'

PAYMENT_STATUS_CHOICES = (
    ('ACTIVE', 'Active'),
    ('CANCELLED', 'Cancelled'),
    ('CANCELED_REVERSAL', 'Canceled_Reversal'),
    ('CLEARED', 'Cleared'),
    ('COMPLETED', 'Completed'),
    ('CREATED', 'Created'),
    ('DECLINED', 'Declined'),
    ('DENIED', 'Denied'),
    ('EXPIRED', 'Expired'),
    ('FAILED', 'Failed'),
    ('PAID', 'Paid'),
    ('PENDING', 'Pending'),
    ('PROCESSED', 'Processed'),
    ('REFUNDED', 'Refunded'),
    ('REFUSED', 'Refused'),
    ('REVERSED', 'Reversed'),
    ('REWARDED', 'Rewarded'),
    ('UNCLAIMED', 'Unclaimed'),
    ('UNCLEARED', 'Uncleared'),
    ('VOIDED', 'Voided'),
)

PAYMENT_REQUEST_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('processed', 'Processed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    ('expired', 'Expired'),
)
