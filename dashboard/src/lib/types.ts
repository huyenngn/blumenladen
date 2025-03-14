export type Purchase = {
  date: string
  product_id: string
  n_bunches: number
  bunch_size: number
  price: number
  percentage: number
}

export type Flower = {
  product_id: string
  purchases: Purchase[]
}
