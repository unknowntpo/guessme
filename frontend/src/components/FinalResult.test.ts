import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FinalResult from './FinalResult.vue'

describe('FinalResult', () => {
  it('should display result label and confidence', () => {
    const wrapper = mount(FinalResult, {
      props: {
        result: 'Cat',
        confidence: 87
      }
    })

    expect(wrapper.text()).toContain('Cat')
    expect(wrapper.text()).toContain('87%')
    expect(wrapper.text()).toContain('Result')
    expect(wrapper.text()).toContain('Confidence')
  })

  it('should show success color by default', () => {
    const wrapper = mount(FinalResult, {
      props: {
        result: 'Cat',
        confidence: 87
      }
    })

    const values = wrapper.findAll('[data-testid="result-value"]')
    expect(values[0].classes()).toContain('text-success')
    expect(values[1].classes()).toContain('text-success')
  })

  it('should have display none when not visible', () => {
    const wrapper = mount(FinalResult, {
      props: {
        result: 'Cat',
        confidence: 87,
        visible: false
      }
    })

    // v-show uses inline style display: none
    expect(wrapper.element.style.display).toBe('none')
  })

  it('should be visible when visible prop is true', () => {
    const wrapper = mount(FinalResult, {
      props: {
        result: 'Cat',
        confidence: 87,
        visible: true
      }
    })

    expect(wrapper.element.style.display).not.toBe('none')
  })
})
