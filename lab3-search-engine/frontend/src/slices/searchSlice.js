import { createSlice } from "@reduxjs/toolkit"

export const searchSlice = createSlice({
  name: "search",
  initialState: {
    results: [],
    duration: null,
    originalImage: {
      data: null,
      name: null
    },
    config: {
      widthRange: [200, 2000],
      heightRange: [200, 2000],
      widthFilter: false,
      heightFilter: false,
      limits: 8,
      color: null
    }
  },
  reducers: {
    setResult: (state, action) => {
      state.results = action.payload.results
      state.duration = action.payload.duration
    },
    setOriginalImage: (state, action) => {
      state.originalImage = action.payload
    },
    setWidthRange: (state, action) => {
      state.config.widthRange = action.payload
    },
    setHeightRange: (state, action) => {
      state.config.heightRange = action.payload
    },
    setLimits: (state, action) => {
      state.config.limits = action.payload
    },
    setWidthFilter: (state, action) => {
      state.config.widthFilter = action.payload
    },
    setHeightFilter: (state, action) => {
      state.config.heightFilter = action.payload
    },
    setColor: (state, action) => {
      state.config.color = action.payload
    }
  }
})

export const selectResult = state => state.search.results
export const selectDuration = state => state.search.duration
export const selectOriginalImage = state => state.search.originalImage
export const selectConfig = state => state.search.config

export const { setResult, setOriginalImage, setWidthRange,
  setHeightRange, setLimits, setWidthFilter, setHeightFilter,
  setColor } = searchSlice.actions
export default searchSlice.reducer
