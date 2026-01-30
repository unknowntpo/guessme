import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import SimpleGameControls from './SimpleGameControls.vue'

describe('SimpleGameControls', () => {
  describe('default state (drawing)', () => {
    it('should show Clear and Send buttons', () => {
      const wrapper = mount(SimpleGameControls, {
        props: { canSubmit: true, isLoading: false }
      })

      expect(wrapper.text()).toContain('Clear')
      expect(wrapper.text()).toContain('Send')
    })

    it('should emit clear event when Clear clicked', async () => {
      const wrapper = mount(SimpleGameControls, {
        props: { canSubmit: true, isLoading: false }
      })

      await wrapper.find('[data-testid="clear-btn"]').trigger('click')
      expect(wrapper.emitted('clear')).toBeTruthy()
    })

    it('should emit send event when Send clicked', async () => {
      const wrapper = mount(SimpleGameControls, {
        props: { canSubmit: true, isLoading: false }
      })

      await wrapper.find('[data-testid="send-btn"]').trigger('click')
      expect(wrapper.emitted('send')).toBeTruthy()
    })
  })

  describe('canSubmit prop', () => {
    it('should disable Send button when canSubmit=false', () => {
      const wrapper = mount(SimpleGameControls, {
        props: { canSubmit: false, isLoading: false }
      })

      const sendBtn = wrapper.find('[data-testid="send-btn"]')
      expect(sendBtn.attributes('disabled')).toBeDefined()
    })

    it('should enable Send button when canSubmit=true', () => {
      const wrapper = mount(SimpleGameControls, {
        props: { canSubmit: true, isLoading: false }
      })

      const sendBtn = wrapper.find('[data-testid="send-btn"]')
      expect(sendBtn.attributes('disabled')).toBeUndefined()
    })
  })

  describe('loading state', () => {
    it('should disable both buttons when loading', () => {
      const wrapper = mount(SimpleGameControls, {
        props: { canSubmit: true, isLoading: true }
      })

      const clearBtn = wrapper.find('[data-testid="clear-btn"]')
      const sendBtn = wrapper.find('[data-testid="send-btn"]')

      expect(clearBtn.attributes('disabled')).toBeDefined()
      expect(sendBtn.attributes('disabled')).toBeDefined()
    })

    it('should show loading text on Send button', () => {
      const wrapper = mount(SimpleGameControls, {
        props: { canSubmit: true, isLoading: true }
      })

      expect(wrapper.find('[data-testid="send-btn"]').text()).toContain('Sending')
    })
  })

  describe('Clear button', () => {
    it('should always be enabled when not loading', () => {
      const wrapper = mount(SimpleGameControls, {
        props: { canSubmit: false, isLoading: false }
      })

      const clearBtn = wrapper.find('[data-testid="clear-btn"]')
      expect(clearBtn.attributes('disabled')).toBeUndefined()
    })
  })
})
