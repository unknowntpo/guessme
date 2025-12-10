import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Timer from './Timer.vue'

describe('Timer', () => {
  it('should display time left', () => {
    const wrapper = mount(Timer, {
      props: { timeLeft: 25, isWarning: false }
    })

    expect(wrapper.text()).toContain('25')
    expect(wrapper.text()).toContain('s')
  })

  it('should have accent background when not warning', () => {
    const wrapper = mount(Timer, {
      props: { timeLeft: 15, isWarning: false }
    })

    expect(wrapper.classes()).toContain('bg-accent')
    expect(wrapper.classes()).not.toContain('bg-error')
  })

  it('should have error background when warning', () => {
    const wrapper = mount(Timer, {
      props: { timeLeft: 5, isWarning: true }
    })

    expect(wrapper.classes()).toContain('bg-error')
    expect(wrapper.classes()).toContain('text-white')
  })
})
