import { Badge, Box, Center, CloseButton, grid, Heading, HStack, Image, SimpleGrid, Text, Tooltip, VStack, Wrap, WrapItem } from "@chakra-ui/react"
import { useEffect } from "react"
import { useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
import { selectDuration, selectOriginalImage, selectResult } from "../slices/searchSlice"
import ConfigTable from "./ConfigTable"

export default function ResultPage() {
  const results = useSelector(selectResult)
  const duration = useSelector(selectDuration)
  const originalImage = useSelector(selectOriginalImage)

  const navigate = useNavigate()
  const returnToIndexPage = () => navigate("/")

  useEffect(() => {
    if (results === null || originalImage.data == null) {
      returnToIndexPage()
    }
  }, [results])

  const combinedResults = [{id: "Original", distance: originalImage.name, url: originalImage.data}, ...results]

  const containerStyle = {
    maxWidth: "1200px",
    margin: "50px auto 50px auto",
    paddingLeft: "50px",
    paddingRight: "50px"
  }

  const colorBoxStyle = {
    userSelect: "none"
  }

  return <VStack style={containerStyle} spacing={10}>
    <VStack align="start" spacing={10} width="100%">
      <VStack align="start">
        <HStack spacing="10px" align="center">
          <Heading>Result</Heading>
          <CloseButton size="lg" onClick={returnToIndexPage} />
        </HStack>
        <Badge>Duration: {duration}</Badge>
      </VStack>
      <ConfigTable />
    </VStack>
    
    <SimpleGrid columns={3} spacing={15} width="100%">
      {combinedResults.map(result => {
        const isOriginal = result.id === "Original"
        const imageSrc = isOriginal ? result.url : process.env.REACT_APP_BACKEND_HOST + result.url
        const bgColor = isOriginal ? "#E2E8F0" : "#F7FAFC"
        return <Box key={result.id} width="100%" borderWidth="1px" borderRadius="lg" bgColor={bgColor} overflow="clip">
          <Center height="300px">
            <Image height="100%" width="100%" src={imageSrc} fit="cover" />
          </Center>
          <Box p="12px">
            <VStack spacing="3px" align="start">
              <Text><b>{result.id}</b></Text>
              <Tooltip label="distance">
                <Text><code>{result.distance}</code></Text>
              </Tooltip>              
              {result.colors &&
                <Wrap paddingTop={2}>
                  {result.colors.map(color => <WrapItem key={color}>
                    <Tooltip label={color}>
                      <Badge bgColor={color} textColor="transparent" style={colorBoxStyle}>XX</Badge>
                    </Tooltip>
                  </WrapItem>)}
                </Wrap>
              }
            </VStack>
          </Box>
        </Box>
      })}
    </SimpleGrid>
  </VStack>
}