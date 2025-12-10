import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PredictionsList from './PredictionsList.vue'
import type { Prediction } from '@/types'

describe('PredictionsList', () => {
  it('should show placeholder when no predictions', () => {
    const wrapper = mount(PredictionsList, {
      props: { predictions: [] }
    })

    expect(wrapper.text()).toContain('Start drawing')
  })

  it('should display predictions sorted by confidence', () => {
    const predictions: Prediction[] = [
      { label: 'Cat', confidence: 87 },
      { label: 'Dog', confidence: 45 },
      { label: 'Bird', confidence: 30 }
    ]

    const wrapper = mount(PredictionsList, {
      props: { predictions }
    })

    const items = wrapper.findAll('[data-testid="prediction-item"]')
    expect(items).toHaveLength(3)

    // First item should have highlight
    expect(items[0].classes()).toContain('bg-accent')

    // Check labels are in order
    expect(items[0].text()).toContain('Cat')
    expect(items[0].text()).toContain('87%')
    expect(items[1].text()).toContain('Dog')
    expect(items[2].text()).toContain('Bird')
  })

  it('should show progress bars with correct width', () => {
    const predictions: Prediction[] = [
      { label: 'Cat', confidence: 75 }
    ]

    const wrapper = mount(PredictionsList, {
      props: { predictions }
    })

    const fill = wrapper.find('[data-testid="progress-fill"]')
    expect(fill.attributes('style')).toContain('width: 75%')
  })

  it('should highlight first item with accent color', () => {
    const predictions: Prediction[] = [
      { label: 'Cat', confidence: 87 },
      { label: 'Dog', confidence: 45 }
    ]

    const wrapper = mount(PredictionsList, {
      props: { predictions }
    })

    const items = wrapper.findAll('[data-testid="prediction-item"]')

    // First item highlighted
    expect(items[0].classes()).toContain('bg-accent')
    expect(items[0].classes()).toContain('border-2')

    // Other items not highlighted
    expect(items[1].classes()).toContain('bg-bg')
    expect(items[1].classes()).not.toContain('bg-accent')
  })
})
