import { mount } from '@vue/test-utils'
import Footer from '../Footer.vue'

describe('Footer.vue', () => {
  it('renders copyright notice', () => {
    const wrapper = mount(Footer)
    expect(wrapper.text()).toMatch(/© 2025 Sistemas Paralelos e Distribuídos/)
  })
})