import axios from 'axios'
import type { Flower } from './types'

axios.defaults.baseURL = 'http://localhost:8080'

async function update_flowers(): Promise<Record<string, any>> {
  try {
    const response = await axios.post('/version')
    return response.data
  } catch (error) {
    console.error(error)
    return { success: false }
  }
}

async function get_last_updated(): Promise<Record<string, any>> {
  try {
    const response = await axios.get('/version')
    return response.data
  } catch (error) {
    console.error(error)
    return { success: false }
  }
}

async function list_flowers(): Promise<Flower[]> {
  try {
    const response = await axios.get('/flowers')
    return response.data as Flower[]
  } catch (error) {
    console.error(error)
    return []
  }
}

async function get_flower(product_id: string): Promise<Flower | null> {
  try {
    const response = await axios.get(`/flowers/${product_id}`)
    return response.data as Flower
  } catch (error) {
    console.error(error)
    return null
  }
}

export { get_flower, get_last_updated, list_flowers, update_flowers }
