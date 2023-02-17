import { module, test } from 'qunit';
import { setupRenderingTest } from 'mysagw/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | filter-modal', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<FilterModal />`);

    assert.dom(this.element).hasText('');

    // Template block usage:
    await render(hbs`
      <FilterModal>
        template block text
      </FilterModal>
    `);

    assert.dom(this.element).hasText('template block text');
  });
});
