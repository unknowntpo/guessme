import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import GameControls from './GameControls.vue'

describe('GameControls', () => {
  it('should show Clear and Submit buttons by default', () => {
    const wrapper = mount(GameControls, {
      props: { gameOver: false }
    })

    expect(wrapper.text()).toContain('Clear')
    expect(wrapper.text()).toContain('Submit')
    expect(wrapper.text()).not.toContain('New Game')
  })

  it('should show New Game button when gameOver', () => {
    const wrapper = mount(GameControls, {
      props: { gameOver: true }
    })

    expect(wrapper.text()).not.toContain('Clear')
    expect(wrapper.text()).not.toContain('Submit')
    expect(wrapper.text()).toContain('New Game')
  })

  it('should emit clear event', async () => {
    const wrapper = mount(GameControls, {
      props: { gameOver: false }
    })

    await wrapper.find('[data-testid="clear-btn"]').trigger('click')
    expect(wrapper.emitted('clear')).toBeTruthy()
  })

  it('should emit submit event', async () => {
    const wrapper = mount(GameControls, {
      props: { gameOver: false }
    })

    await wrapper.find('[data-testid="submit-btn"]').trigger('click')
    expect(wrapper.emitted('submit')).toBeTruthy()
  })

  it('should emit newGame event', async () => {
    const wrapper = mount(GameControls, {
      props: { gameOver: true }
    })

    await wrapper.find('[data-testid="new-game-btn"]').trigger('click')
    expect(wrapper.emitted('newGame')).toBeTruthy()
  })
})
