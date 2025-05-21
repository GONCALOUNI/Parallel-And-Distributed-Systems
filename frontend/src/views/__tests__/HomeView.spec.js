import { mount } from '@vue/test-utils'
import HomeView from '../HomeView.vue'

describe('HomeView.vue', () => {
  it('navigates to /store on click', async () => {
    const push = vi.fn()
    const wrapper = mount(HomeView, {
      global: { mocks: { $router: { push } } }
    })
    await wrapper.find('button').trigger('click')
    expect(push).toHaveBeenCalledWith('/store')
  })

  it('renders welcome text', () => {
    const wrapper = mount(HomeView)
    expect(wrapper.text()).toContain('Seja bem-vind@ ao KVerse!')
  })
})