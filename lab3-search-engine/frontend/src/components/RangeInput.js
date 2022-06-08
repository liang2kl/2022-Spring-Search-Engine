import { Checkbox, HStack, RangeSlider, RangeSliderFilledTrack, RangeSliderThumb, RangeSliderTrack, Text, VStack } from "@chakra-ui/react"
import { useState } from "react"

export default function RangeInput(props) {

  const [value, setValue] = useState(props.value ?? [])

  return <HStack width="100%" align="start">
    {props.label && 
    <Checkbox isChecked={props.checked} width={100}
      onChange={(e) => props.onToggle(e.target.checked)}
      disabled={props.disabled}
    >
      <b>{props.label}</b>
    </Checkbox>}
    <VStack width="100%">
      <RangeSlider min={props.min} max={props.max}
        step={props.step} defaultValue={props.value}
        onChange={(value) => setValue(value)}
        onChangeEnd={props.onChangeEnd}
        isDisabled={!props.checked || props.disabled}
      >
        <RangeSliderTrack>
          <RangeSliderFilledTrack />
        </RangeSliderTrack>
        <RangeSliderThumb boxSize={5} index={0} />
        <RangeSliderThumb boxSize={5} index={1} />
      </RangeSlider>
      <HStack width="100%" justify="space-between">
        <Text><code>{props.min}</code></Text>
        {props.checked && <Text><code>[{value[0]}, {value[1]}]</code></Text>}
        <Text><code>{props.max}</code></Text>
      </HStack>
    </VStack>
  </HStack>

}