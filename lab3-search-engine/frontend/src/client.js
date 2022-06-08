import axios from "axios"

axios.defaults.baseURL = process.env.REACT_APP_BACKEND_HOST

export function query(base64EncodedImage, limit, widthRange, heightRange, color) {
  let params = {
    limit: limit
  }
  if (widthRange) {
    params.width = widthRange.join(",")
  }
  if (heightRange) {
    params.height = heightRange.join(",")
  }
  if (color) {
    params.color = color
  }
  console.log(params)
  return axios.post("/q", base64EncodedImage, {
    params: params
  })
}
