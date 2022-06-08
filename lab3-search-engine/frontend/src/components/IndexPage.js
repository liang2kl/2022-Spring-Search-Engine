import { ArrowUpIcon, ChevronDownIcon, SearchIcon } from "@chakra-ui/icons"
import { Box, Button, Checkbox, Divider, Heading, HStack, Image as ImageComponent,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  NumberDecrementStepper, NumberIncrementStepper, NumberInput,
  NumberInputField, NumberInputStepper, RangeSlider, RangeSliderFilledTrack, RangeSliderThumb, RangeSliderTrack, Spinner, Text, useToast,
  VStack } from "@chakra-ui/react"
import { useEffect, useRef, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
import { query } from "../client"
import { selectConfig, selectOriginalImage, setColor, setHeightFilter, setHeightRange, setLimits, setOriginalImage, setResult, setWidthFilter, setWidthRange } from "../slices/searchSlice"
import RangeInput from "./RangeInput"

export default function IndexPage() {

  const imageInputRef = useRef()
  const dispatch = useDispatch()
  const toast = useToast()
  const navigate = useNavigate()
  const originalImage = useSelector(selectOriginalImage)
  const [isLoading, setIsLoading] = useState(false)
  const config = useSelector(selectConfig)

  useEffect(() => {
    const imageDataStr = localStorage.getItem("originalImage")
    if (imageDataStr) {
      const imageData = JSON.parse(imageDataStr)
      if (imageData) {
        dispatch(setOriginalImage(imageData))
      }
    }
  }, [])

  function saveUploadedImg() {
    const input = imageInputRef.current
    if (input.files && input.files[0]) {
      var reader = new FileReader()
      const name = input.files[0].name

      reader.onload = (e) => {
        const imgURL = e.target.result
        var image = new Image()
        image.src = imgURL
        
        const imageData = { data: imgURL, name: name }
        dispatch(setOriginalImage(imageData))
        localStorage.setItem("originalImage", JSON.stringify(imageData))
      }
      reader.readAsDataURL(input.files[0])
    }
    // reset
    input.value = null
  }

  function sendQuery() {
    setIsLoading(true)
    
    const base64String = originalImage.data.replace(/^data:image\/(png|jpg|jpeg);base64,/, "")
    query(base64String, config.limits,
      config.widthFilter ? config.widthRange : null,
      config.heightFilter ? config.heightRange : null,
      config.color ? config.color.slice(1) : null
    )
      .then(res => {
        setIsLoading(false)
        dispatch(setResult(res.data))
        navigate("/q")
      })
      .catch(err => {
        setIsLoading(false)
        toast({
          title: "Error",
          description: err.message,
          status: "error",
          duration: 2000,
          isClosable: true
        })
      })
  }

  const availableLimits = [1, 8, 20, 26, 32, 38]
  const availableColors = ["#EEEEEE", "#AAAAAA", "#444444", "#F56565",
    "#ED8936", "#ECC94B", "#48BB78", "#38B2AC", "#4299E1", "#0BC5EA",
    "#9F7AEA", "#ED64A6"
  ]

  const containerStyle = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    userSelect: "none",
    paddingLeft: "50px",
    paddingRight: "50px",
    maxWidth: "800px",
    marginLeft: "auto",
    marginRight: "auto"
  }

  const inputStyle = {
    display: "none"
  }

  const colorBoxStyle = {
    borderWidth: "2px",
    borderRadius: "8px",
    borderColor: "#00000033"
  }

  return <Box style={containerStyle}>
    <VStack spacing="40px" minWidth="500px">
      <HStack spacing="60px" justify="space-between" width="100%">
        <Heading>Image Search</Heading>
        <Button
          leftIcon={<ArrowUpIcon />}
          onClick={() => { imageInputRef.current.click() }}
          disabled={isLoading}
        >
          Upload
        </Button>
      </HStack>
      {originalImage.data && <VStack spacing="20px" width="100%">
        <Box width="100%" borderWidth="1px" borderRadius="lg" overflow="clip">
          <Box width="100%" bgColor="#F7FAFC">
            <ImageComponent width="100%" maxWidth="700px" src={originalImage.data} fit="cover" />
            <Text p="15px" alignSelf="start"><code>{originalImage.name}</code></Text>
          </Box>

          <Divider />

          <VStack p="15px" marginTop={15} spacing="15px" align="end" width="100%" paddingTop="10px">
            <RangeInput min={0} max={4000} step={200}
              value={config.widthRange} label="Width"
              onChangeEnd={(value) => dispatch(setWidthRange(value))}
              checked={config.widthFilter}
              onToggle={(checked) => dispatch(setWidthFilter(checked))}
              disabled={isLoading}
            />
            <RangeInput min={0} max={4000} step={200}
              value={config.heightRange} label="Height"
              onChangeEnd={(value) => dispatch(setHeightRange(value))}
              checked={config.heightFilter}
              onToggle={(checked) => dispatch(setHeightFilter(checked))}
              disabled={isLoading}
            />
            <HStack>
              <Menu>
                <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                  <HStack>
                    <Text>Color: </Text>
                    {config.color && <Box style={colorBoxStyle} bgColor={config.color} textColor="#00000000" >
                      <code>{config.color}</code>
                    </Box>}
                    {!config.color && <Box>None</Box>}
                  </HStack>
                </MenuButton>
                <MenuList>
                  {availableColors.map((c) => {
                    return <MenuItem key={c} onClick={() => dispatch(setColor(c))}>
                      <Box style={colorBoxStyle} bgColor={c} width="100%" textColor="#00000000">{c}</Box>
                    </MenuItem>
                  })}
                  <MenuItem onClick={() => dispatch(setColor(null))}>
                    None
                  </MenuItem>
                </MenuList>
              </Menu>

              <Menu>
                <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                  Limits: {config.limits}
                </MenuButton>
                <MenuList>
                  {availableLimits.map((l) => {
                    return <MenuItem key={l} onClick={() => dispatch(setLimits(l))}>
                      {l}
                    </MenuItem>
                  })}
                </MenuList>
              </Menu>

              <Button colorScheme="blue" disabled={isLoading}
                leftIcon={isLoading ? null : <SearchIcon />}
                onClick={sendQuery} rightIcon={isLoading ? <Spinner /> : null}
              >
                Search
              </Button>
            </HStack>
          </VStack>

        </Box>

      </VStack>}

        
    </VStack>
    <input style={inputStyle} ref={imageInputRef}
      type="file" accept="image/jpeg" onChange={saveUploadedImg}/>
  </Box>
}