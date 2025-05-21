import { mount, RouterLinkStub } from '@vue/test-utils'
import Navbar from '../Navbar.vue'

beforeAll(() => {
  window.matchMedia = window.matchMedia || function() {
    return {
      matches: false,
      addListener: () => {},
      removeListener: () => {}
    }
  }
})

describe('Navbar.vue', () => {
  it('renders brand and links', () => {
    const wrapper = mount(Navbar, {
      global: {
        stubs: { 'router-link': RouterLinkStub }
      }
    })
    expect(wrapper.find('.navbar-brand').text()).toBe('KVerse')
    expect(wrapper.findAll('.nav-link')).toHaveLength(3)
  })
})