export enum POStatus {
  DRAFT = "draft",
  APPROVED = "approved",
  SENT = "sent",
  PARTIALLY_RECEIVED = "partially_received",
  RECEIVED = "received",
  CANCELLED = "cancelled",
  CLOSED = "closed",
}

export enum TransferStatus {
  DRAFT = "draft",
  PENDING_APPROVAL = "pending_approval",
  APPROVED = "approved",
  IN_TRANSIT = "in_transit",
  RECEIVED = "received",
  CANCELLED = "cancelled",
}

export enum TransactionType {
  GOODS_RECEIVED = "goods_received",
  SALE = "sale",
  MANUAL_ADJUSTMENT = "manual_adjustment",
  TRANSFER_OUT = "transfer_out",
  TRANSFER_IN = "transfer_in",
  DAMAGE = "damage",
  EXPIRY = "expiry",
  RETURN = "return",
  RESERVATION = "reservation",
  ALLOCATION = "allocation",
  RELEASE = "release",
}
