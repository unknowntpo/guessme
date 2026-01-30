import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ResultDisplay from './ResultDisplay.vue'

describe('ResultDisplay', () => {
  describe('when visible', () => {
    it('should display digit result', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 87, visible: true }
      })
      expect(wrapper.text()).toContain('7')
    })

    it('should display confidence percentage', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 3, confidence: 95, visible: true }
      })
      expect(wrapper.text()).toContain('95%')
    })

    it('should show Try Again button', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 87, visible: true }
      })
      expect(wrapper.find('[data-testid="try-again-btn"]').exists()).toBe(true)
    })

    it('should emit tryAgain when button clicked', async () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 87, visible: true }
      })
      await wrapper.find('[data-testid="try-again-btn"]').trigger('click')
      expect(wrapper.emitted('tryAgain')).toBeTruthy()
    })
  })

  describe('confidence colors', () => {
    it('should use success color for high confidence (>=70%)', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 70, visible: true }
      })
      const confidenceEl = wrapper.find('[data-testid="confidence-value"]')
      expect(confidenceEl.classes()).toContain('text-success')
    })

    it('should use success color for very high confidence', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 95, visible: true }
      })
      const confidenceEl = wrapper.find('[data-testid="confidence-value"]')
      expect(confidenceEl.classes()).toContain('text-success')
    })

    it('should use accent color for medium confidence (40-69%)', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 50, visible: true }
      })
      const confidenceEl = wrapper.find('[data-testid="confidence-value"]')
      expect(confidenceEl.classes()).toContain('text-accent')
    })

    it('should use accent color for 40% confidence', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 40, visible: true }
      })
      const confidenceEl = wrapper.find('[data-testid="confidence-value"]')
      expect(confidenceEl.classes()).toContain('text-accent')
    })

    it('should use accent color for 69% confidence', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 69, visible: true }
      })
      const confidenceEl = wrapper.find('[data-testid="confidence-value"]')
      expect(confidenceEl.classes()).toContain('text-accent')
    })

    it('should use error color for low confidence (<40%)', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 30, visible: true }
      })
      const confidenceEl = wrapper.find('[data-testid="confidence-value"]')
      expect(confidenceEl.classes()).toContain('text-error')
    })

    it('should use error color for 39% confidence', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 39, visible: true }
      })
      const confidenceEl = wrapper.find('[data-testid="confidence-value"]')
      expect(confidenceEl.classes()).toContain('text-error')
    })
  })

  describe('progress bar', () => {
    it('should have correct width percentage', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 87, visible: true }
      })
      const bar = wrapper.find('[data-testid="confidence-bar"]')
      expect(bar.attributes('style')).toContain('width: 87%')
    })
  })

  describe('visibility', () => {
    it('should be hidden when visible=false', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 87, visible: false }
      })
      expect(wrapper.find('[data-testid="result-card"]').exists()).toBe(false)
    })

    it('should be shown when visible=true', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: 7, confidence: 87, visible: true }
      })
      expect(wrapper.find('[data-testid="result-card"]').exists()).toBe(true)
    })
  })

  describe('error state', () => {
    it('should display error message when provided', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: null, confidence: 0, visible: true, error: 'Connection failed' }
      })
      expect(wrapper.text()).toContain('Connection failed')
    })

    it('should hide digit when error is present', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: null, confidence: 0, visible: true, error: 'Connection failed' }
      })
      expect(wrapper.find('[data-testid="digit-value"]').exists()).toBe(false)
    })

    it('should still show Try Again button on error', () => {
      const wrapper = mount(ResultDisplay, {
        props: { digit: null, confidence: 0, visible: true, error: 'Connection failed' }
      })
      expect(wrapper.find('[data-testid="try-again-btn"]').exists()).toBe(true)
    })
  })
})
