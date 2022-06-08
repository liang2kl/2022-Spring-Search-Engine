import "./App.css"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import IndexPage from "./components/IndexPage"
import ResultPage from "./components/ResultPage"

function App() {
  return <>
    <BrowserRouter basename="/">
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/q" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  </>
}

export default App
